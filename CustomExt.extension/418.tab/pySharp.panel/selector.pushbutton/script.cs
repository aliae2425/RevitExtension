using System;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB;

namespace selector.pushbutton {
    
    [Transaction(TransactionMode.Manual)]
   public class Command : IExternalCommand {
      public Result Execute(ExternalCommandData revit,
                            ref string message, ElementSet elements) {
         UIApplication uiApp = commandData.Application;
         UIDocument uidoc = uiApp.ActiveUIDocument;
         Application app = uiApp.Application;
         Document doc = uidoc.Document;

         

         return Result.Succeeded;

      }
   }
}