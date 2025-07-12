# -*- coding: utf-8 -*-

# ------------------------------- info pyrevit ------------------------------- #
__title__ = "Échappée Escalier"
__doc__ = """
    version : 1.3.0
    Date : 12.07.2025
    __________________
    Sélectionne un escalier et crée un volume d'échappée qui respecte 
    la hauteur libre de 2m au-dessus de chaque nez de marche
    avec une marge de sécurité de 20cm horizontalement
"""
__author__ = 'Aliae'                               
__min_revit_ver__ = 2021                                       
__max_revit_ver__ = 2026

# Imports pyRevit standards
from pyrevit import forms, revit, DB

# Variables globales pour pyRevit
doc = revit.doc
uidoc = revit.uidoc

def create_stair_escape_volume():
    """
    Crée un volume d'échappée au-dessus d'un escalier sélectionné
    Respecte la hauteur libre de 2m au-dessus de chaque nez de marche
    """
    try:
        stair = None
        
        # Vérifier d'abord s'il y a déjà un escalier sélectionné
        selection = uidoc.Selection
        selected_ids = selection.GetElementIds()
        
        if selected_ids:
            # Chercher un escalier dans la sélection actuelle
            for element_id in selected_ids:
                element = doc.GetElement(element_id)
                if element and element.Category:
                    # Vérifier si c'est un escalier de plusieurs façons
                    is_stair = (
                        element.Category.Id == DB.ElementId(DB.BuiltInCategory.OST_Stairs) or
                        element.Category.Name == "Stairs" or
                        "Stair" in str(element.Category.Name)
                    )
                    if is_stair:
                        stair = element
                        break
        
        # Si aucun escalier n'est présélectionné, demander à l'utilisateur d'en sélectionner un
        if not stair:
            try:
                # Demander à l'utilisateur de sélectionner un escalier
                stair_ref = selection.PickObject(
                    DB.ObjectType.Element,
                    "Sélectionnez un escalier"
                )
                
                if not stair_ref:
                    forms.alert("Aucun escalier sélectionné.", title="Erreur")
                    return
                    
                # Récupérer l'élément escalier
                stair = doc.GetElement(stair_ref)
                
            except Exception as pick_error:
                forms.alert(
                    "Sélection annulée ou erreur lors de la sélection.",
                    title="Erreur de sélection"
                )
                return
        
        # Vérifier que c'est bien un escalier
        if not stair or not stair.Category:
            forms.alert("L'élément sélectionné n'est pas valide.", title="Erreur")
            return
            
        # Vérification multiple pour s'assurer que c'est un escalier
        is_stair = (
            stair.Category.Id == DB.ElementId(DB.BuiltInCategory.OST_Stairs) or
            stair.Category.Name == "Stairs" or
            "Stair" in str(stair.Category.Name) or
            "Escalier" in str(stair.Category.Name)
        )
        
        if not is_stair:
            forms.alert(
                "L'élément sélectionné n'est pas un escalier.\n\n"
                "Catégorie détectée : {}".format(stair.Category.Name),
                title="Erreur de type d'élément"
            )
            return
        
        # Récupérer la bounding box de l'escalier
        bbox = stair.get_BoundingBox(None)
        if not bbox:
            forms.alert("Impossible de récupérer les dimensions de l'escalier.", title="Erreur")
            return
        
        # Récupérer les propriétés de l'escalier
        try:
            # Tenter de récupérer la hauteur de marche et le giron
            riser_height = None
            tread_depth = None
            
            # Récupérer les paramètres de l'escalier
            for param in stair.Parameters:
                param_name = param.Definition.Name
                if "Riser" in param_name and "Height" in param_name:
                    riser_height = param.AsDouble()
                elif "Tread" in param_name and ("Depth" in param_name or "Width" in param_name):
                    tread_depth = param.AsDouble()
                elif "Hauteur" in param_name and "Marche" in param_name:
                    riser_height = param.AsDouble()
                elif "Giron" in param_name or ("Profondeur" in param_name and "Marche" in param_name):
                    tread_depth = param.AsDouble()
            
            # Valeurs par défaut si non trouvées
            if not riser_height:
                riser_height = 0.583  # 17.8cm en pieds (valeur standard)
            if not tread_depth:
                tread_depth = 0.958  # 29.2cm en pieds (valeur standard)
                
        except:
            # Valeurs par défaut en cas d'erreur
            riser_height = 0.583  # 17.8cm en pieds
            tread_depth = 0.958  # 29.2cm en pieds
        
        # Calculer les dimensions du volume englobant
        min_point = bbox.Min
        max_point = bbox.Max
        
        # Ajouter une marge de sécurité (20cm de chaque côté horizontalement)
        margin = 0.65617  # 20cm en pieds
        
        # Hauteur d'échappée : 2m au-dessus de chaque marche
        escape_height = 6.56168  # 2m en pieds
        
        # Calculer le nombre de marches approximatif
        total_height = max_point.Z - min_point.Z
        num_risers = int(total_height / riser_height) if riser_height > 0 else 10
        
        # Déterminer la direction principale de l'escalier
        width = max_point.X - min_point.X
        depth = max_point.Y - min_point.Y
        is_horizontal = width > depth  # True si l'escalier va dans la direction X
        
        # Points ajustés avec marge horizontale
        adjusted_min = DB.XYZ(
            min_point.X - margin,
            min_point.Y - margin,
            min_point.Z
        )
        adjusted_max = DB.XYZ(
            max_point.X + margin,
            max_point.Y + margin,
            max_point.Z + escape_height
        )
        
        # Début de la transaction
        with revit.Transaction("Créer volume d'échappée escalier"):
            
            # Créer une géométrie composite pour représenter l'échappée
            solids = []
            
            # Créer des segments de volume pour chaque zone de marche
            for i in range(num_risers + 1):  # +1 pour inclure le palier final
                # Calculer la position et hauteur de ce segment
                if is_horizontal:
                    # Escalier dans la direction X
                    segment_length = (adjusted_max.X - adjusted_min.X) / (num_risers + 1)
                    segment_start_x = adjusted_min.X + (i * segment_length)
                    segment_end_x = segment_start_x + segment_length
                    segment_start_y = adjusted_min.Y
                    segment_end_y = adjusted_max.Y
                else:
                    # Escalier dans la direction Y
                    segment_length = (adjusted_max.Y - adjusted_min.Y) / (num_risers + 1)
                    segment_start_x = adjusted_min.X
                    segment_end_x = adjusted_max.X
                    segment_start_y = adjusted_min.Y + (i * segment_length)
                    segment_end_y = segment_start_y + segment_length
                
                # Hauteur de base de ce segment (suivant la pente de l'escalier)
                base_height = adjusted_min.Z + (i * riser_height)
                top_height = base_height + escape_height
                
                # Créer les points du rectangle de base pour ce segment
                segment_points = [
                    DB.XYZ(segment_start_x, segment_start_y, base_height),
                    DB.XYZ(segment_end_x, segment_start_y, base_height),
                    DB.XYZ(segment_end_x, segment_end_y, base_height),
                    DB.XYZ(segment_start_x, segment_end_y, base_height),
                    DB.XYZ(segment_start_x, segment_start_y, base_height)  # Fermer le profil
                ]
                
                # Créer les lignes pour le profil rectangulaire de ce segment
                segment_curve_loop = DB.CurveLoop()
                for j in range(len(segment_points) - 1):
                    line = DB.Line.CreateBound(segment_points[j], segment_points[j + 1])
                    segment_curve_loop.Append(line)
                
                # Calculer la hauteur d'extrusion pour ce segment
                segment_height = top_height - base_height
                
                # Créer la géométrie par extrusion pour ce segment
                try:
                    segment_solid = DB.GeometryCreationUtilities.CreateExtrusionGeometry(
                        [segment_curve_loop],
                        DB.XYZ.BasisZ,  # Direction vers le haut
                        segment_height
                    )
                    solids.append(segment_solid)
                except:
                    pass  # Ignorer les segments qui échouent
            
            # Fusionner tous les solides en un seul volume
            if solids:
                # Commencer avec le premier solide
                combined_solid = solids[0]
                
                # Fusionner avec les autres solides
                for i in range(1, len(solids)):
                    try:
                        combined_solid = DB.BooleanOperationsUtils.ExecuteBooleanOperation(
                            combined_solid, solids[i], DB.BooleanOperationsType.Union
                        )
                    except:
                        pass  # Continuer même si la fusion échoue
                
                # Créer un DirectShape pour contenir la géométrie
                direct_shape = DB.DirectShape.CreateElement(
                    doc, 
                    DB.ElementId(DB.BuiltInCategory.OST_GenericModel)
                )
                direct_shape.ApplicationId = "StairEscapeApp"
                direct_shape.ApplicationDataId = "StairEscape_v1.0"
                direct_shape.SetShape([combined_solid])
            else:
                # Fallback : créer un volume simple si la méthode avancée échoue
                base_points = [
                    DB.XYZ(adjusted_min.X, adjusted_min.Y, adjusted_min.Z),
                    DB.XYZ(adjusted_max.X, adjusted_min.Y, adjusted_min.Z),
                    DB.XYZ(adjusted_max.X, adjusted_max.Y, adjusted_min.Z),
                    DB.XYZ(adjusted_min.X, adjusted_max.Y, adjusted_min.Z),
                    DB.XYZ(adjusted_min.X, adjusted_min.Y, adjusted_min.Z)
                ]
                
                curve_loop = DB.CurveLoop()
                for i in range(len(base_points) - 1):
                    line = DB.Line.CreateBound(base_points[i], base_points[i + 1])
                    curve_loop.Append(line)
                
                height = adjusted_max.Z - adjusted_min.Z
                solid = DB.GeometryCreationUtilities.CreateExtrusionGeometry(
                    [curve_loop], DB.XYZ.BasisZ, height
                )
                
                direct_shape = DB.DirectShape.CreateElement(
                    doc, DB.ElementId(DB.BuiltInCategory.OST_GenericModel)
                )
                direct_shape.ApplicationId = "StairEscapeApp"
                direct_shape.ApplicationDataId = "StairEscape_v1.0"
                direct_shape.SetShape([solid])
            
            # Nommer l'élément
            try:
                direct_shape.Name = "Volume Échappée - {}".format(stair.Name if hasattr(stair, 'Name') else "Escalier")
            except:
                pass
            
            # Modifier l'apparence graphique : orange avec 40% de transparence
            try:
                # Créer un override graphique
                override_settings = DB.OverrideGraphicSettings()
                
                # Définir la couleur orange (RGB: 255, 165, 0)
                orange_color = DB.Color(255, 165, 0)
                override_settings.SetSurfaceForegroundPatternColor(orange_color)
                override_settings.SetSurfaceBackgroundPatternColor(orange_color)
                override_settings.SetProjectionLineColor(orange_color)
                override_settings.SetCutLineColor(orange_color)
                override_settings.SetCutForegroundPatternColor(orange_color)
                override_settings.SetCutBackgroundPatternColor(orange_color)
                
                # Définir la transparence à 40% (valeur 60 sur une échelle de 0-100)
                override_settings.SetSurfaceTransparency(60)
                
                # Appliquer l'override à l'élément dans toutes les vues
                views = DB.FilteredElementCollector(doc).OfClass(DB.View).ToElements()
                for view in views:
                    if hasattr(view, 'SetElementOverrides') and not view.IsTemplate:
                        try:
                            view.SetElementOverrides(direct_shape.Id, override_settings)
                        except:
                            pass  # Ignorer si la vue ne supporte pas les overrides
                            
            except Exception as graphics_error:
                pass  # Continuer même si la modification graphique échoue
        
        # Calculer les dimensions en mètres pour l'affichage
        width_m = (adjusted_max.X - adjusted_min.X) / 3.28084
        depth_m = (adjusted_max.Y - adjusted_min.Y) / 3.28084
        total_height_m = (adjusted_max.Z - adjusted_min.Z) / 3.28084
        escape_height_m = escape_height / 3.28084
        
    except Exception as e:
        forms.alert(
            "Erreur lors de la création du volume d'échappée :\n\n{}".format(str(e)),
            title="Erreur"
        )

# Point d'entrée principal
if __name__ == '__main__':
    # Vérifier que nous sommes dans un document Revit valide
    if not doc:
        forms.alert("Aucun document Revit actif trouvé.", title="Erreur")
    elif doc.IsReadOnly:
        forms.alert("Le document est en lecture seule.", title="Erreur")
    else:
        # Lancer directement la fonction d'échappée d'escalier
        create_stair_escape_volume()