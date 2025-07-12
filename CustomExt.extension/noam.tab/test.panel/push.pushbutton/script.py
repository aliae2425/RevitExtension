# -*- coding: utf-8 -*-

# ------------------------------- info pyrevit ------------------------------- #
__title__ = "Encapsulation Escalier"
__doc__ = """
    version : 1.2.0
    Date : 12.07.2025
    __________________
    Sélectionne un escalier et crée un volume rectangulaire qui l'encapsule 
    avec une marge de sécurité de 20cm
"""
__author__ = 'Aliae'                               
__min_revit_ver__ = 2021                                       
__max_revit_ver__ = 2026

# Imports pyRevit standards
from pyrevit import forms, revit, DB

# Variables globales pour pyRevit
doc = revit.doc
uidoc = revit.uidoc

def create_stair_encapsulation_volume():
    """
    Crée un volume qui encapsule un escalier sélectionné
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
        
        # Calculer les dimensions du volume englobant
        min_point = bbox.Min
        max_point = bbox.Max
        
        # Ajouter une marge de sécurité (20cm de chaque côté)
        margin = 0.65617  # 20cm en pieds
        
        # Points ajustés avec marge
        adjusted_min = DB.XYZ(
            min_point.X - margin,
            min_point.Y - margin,
            min_point.Z - margin
        )
        adjusted_max = DB.XYZ(
            max_point.X + margin,
            max_point.Y + margin,
            max_point.Z + margin
        )
        
        # Début de la transaction
        with revit.Transaction("Créer volume d'encapsulation escalier"):
            
            # Créer les points du rectangle de base
            base_points = [
                DB.XYZ(adjusted_min.X, adjusted_min.Y, adjusted_min.Z),
                DB.XYZ(adjusted_max.X, adjusted_min.Y, adjusted_min.Z),
                DB.XYZ(adjusted_max.X, adjusted_max.Y, adjusted_min.Z),
                DB.XYZ(adjusted_min.X, adjusted_max.Y, adjusted_min.Z),
                DB.XYZ(adjusted_min.X, adjusted_min.Y, adjusted_min.Z)  # Fermer le profil
            ]
            
            # Créer les lignes pour le profil rectangulaire
            curve_loop = DB.CurveLoop()
            for i in range(len(base_points) - 1):
                line = DB.Line.CreateBound(base_points[i], base_points[i + 1])
                curve_loop.Append(line)
            
            # Calculer la hauteur d'extrusion
            height = adjusted_max.Z - adjusted_min.Z
            
            # Créer la géométrie par extrusion
            solid = DB.GeometryCreationUtilities.CreateExtrusionGeometry(
                [curve_loop],
                DB.XYZ.BasisZ,  # Direction vers le haut
                height
            )
            
            # Créer un DirectShape pour contenir la géométrie
            direct_shape = DB.DirectShape.CreateElement(
                doc, 
                DB.ElementId(DB.BuiltInCategory.OST_GenericModel)
            )
            direct_shape.ApplicationId = "StairEncapsulationApp"
            direct_shape.ApplicationDataId = "StairEncapsulation_v1.0"
            direct_shape.SetShape([solid])
            
            # Nommer l'élément
            try:
                direct_shape.Name = "Volume Encapsulation - {}".format(stair.Name if hasattr(stair, 'Name') else "Escalier")
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
        height_m = height / 3.28084
        
    except Exception as e:
        forms.alert(
            "Erreur lors de la création du volume d'encapsulation :\n\n{}".format(str(e)),
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
        # Lancer directement la fonction d'encapsulation d'escalier
        create_stair_encapsulation_volume()