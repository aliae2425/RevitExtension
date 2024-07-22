using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace FamillyBrowservV2
{
    /// <summary>
    /// Logique d'interaction pour MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private bool _isLightTheme = true;
        public MainWindow()
        {
            InitializeComponent();
        }

        private void ToggleButton_Checked(object sender, RoutedEventArgs e)
        {
            _isLightTheme = !_isLightTheme;
            string newThemePath = _isLightTheme ? "/Themes/LightTheme.xaml" : "/Themes/DarkTheme.xaml";
            var newTheme = (ResourceDictionary)Application.LoadComponent(resourceLocator: new Uri(newThemePath, UriKind.Relative));
            Application.Current.Resources.MergedDictionaries.RemoveAt(2);
            Application.Current.Resources.MergedDictionaries.Add(newTheme);
        }

        private void CloseApp(object sender, RoutedEventArgs e)
        {
            System.Windows.Application.Current.Shutdown();
        }

    }
}
