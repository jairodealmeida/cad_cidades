from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *
from qgis.utils import iface
from .usage_logging import log_usage
from .resources_rc import *

class CADCidades:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.toolbar = None
        self.settings_dialog = None

        # Default values for settings
        self.layer_id = "BR_Municipios_2021"
        self.attribute = "CD_MUN"
        self.ids = "1100924"
        self.licenced = "..."

    def initGui(self):

        # Criar um QVBoxLayout para organizar os componentes
        layout = QVBoxLayout()

        # Create a toolbar button and connect it to a function
        self.toolbar = self.iface.addToolBar("CADCidades")
        self.toolbar.setFixedWidth(350)

        # Create the QLineEdit widget for the input text box
        self.ids_input = QLineEdit(self.ids)
        self.ids_input.returnPressed.connect(self.feature_ids_input)
        # Create a new QWidget for the input text box
        #self.widget = QWidget()
        #self.widget.setLayout(QVBoxLayout())
        #self.widget.layout().addWidget(self.ids_input)
        layout.addWidget(self.ids_input)

        # Create a new QToolBar and add the input text box widget to it
        #self.toolbar.addWidget(self.widget)
        #self.widget = QWidget()
        
        select_features_icon = QIcon(":/icons/select_features.png")
        self.action = QAction(select_features_icon, "Selecionar", self.iface.mainWindow())
        self.action.triggered.connect(self.feature_ids_input)
        self.toolbar.addAction(self.action)
        #self.widget.addAction(self.action)

        config_icon = QIcon(':/icons/config.png')
        self.action = QAction(config_icon, "CADCidades", self.iface.mainWindow())
        self.action.triggered.connect(self.show_settings_dialog)
        self.toolbar.addAction(self.action)
        #self.widget.addAction(self.action)

        #layout.addWidget(self.widget)
        
        widget = QWidget()
        widget.setLayout(layout)
        # Definir o widget como o layout do QToolBar
        self.toolbar.addWidget(widget)

    def unload(self):
        # This method is called when the plugin is unloaded
        QCoreApplication.instance().aboutToQuit.connect(self.cleanup)
    
    def cleanup(self):
        # Perform any necessary cleanup here
        pass

    def show_settings_dialog(self):
        # Create a dialog to edit plugin settings
        self.settings_dialog = QDialog(self.iface.mainWindow())
        self.settings_dialog.setWindowTitle("CADCidades Settings")
        layout = QVBoxLayout()

        # Add a text field to enter the layer ID
        layer = iface.activeLayer()  # Get a reference to the active layer
        if layer:
            self.layer_id_input = layer.name()    
        layer_id_label = QLabel("Layer ID:")
        self.layer_id_input = QLineEdit(self.layer_id)
        layout.addWidget(layer_id_label)
        layout.addWidget(self.layer_id_input)

        # Add a text field to enter the attribute name
        attribute_label = QLabel("Attribute:")
        self.attribute_input = QLineEdit(self.attribute)
        layout.addWidget(attribute_label)
        layout.addWidget(self.attribute_input)

        plugin_name = "CADCidades QGIS"
        self.licenced = log_usage(plugin_name, "Inicialização")
        licenced_label = QLabel(self.licenced)
        layout.addWidget(licenced_label)
        

        # Add OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.settings_dialog.reject)
        layout.addWidget(button_box)

        self.settings_dialog.setLayout(layout)
        self.settings_dialog.exec_()

    def show_input_code_dialog(self):
        # Create a dialog to edit plugin settings
        self.input_code_dialog = QDialog(self.iface.mainWindow())
        self.input_code_dialog.setWindowTitle("Entre com o CODIGO do Lote")
        layout = QVBoxLayout()

        input_code_label = QLabel("CODIGO:")
        self.ids_input = QLineEdit(self.ids)
        layout.addWidget(input_code_label)
        layout.addWidget(self.ids_input)

        help_label = QLabel("Para destacar mais de uma pode colocar o Codigo separado por virgulas ex: 1100974,1100304")
        layout.addWidget(help_label)
        # Add OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.feature_ids_input)
        button_box.rejected.connect(self.input_code_dialog.reject)
        layout.addWidget(button_box)

        self.input_code_dialog.setLayout(layout)
        self.input_code_dialog.exec_()


    def save_settings(self):
        # Save the plugin settings and close the dialog
        self.layer_id = self.layer_id_input.text()
        self.attribute = self.attribute_input.text()
        self.settings_dialog.accept()


    def feature_ids_input(self):
        self.ids = self.ids_input.text()
        #QMessageBox.warning(self.iface.mainWindow(), "Info", " settings.{}".format(self.ids))
        #self.input_code_dialog.accept()
        run(self)

def run(self):
    plugin_name = "CADCidades QGIS"
   

    # Main logic of the plugin
    if not self.layer_id or not self.attribute:
        # Show an error message if settings are not defined
        QMessageBox.warning(self.iface.mainWindow(), "Plugin Settings", "Layer ID and attribute must be defined in the plugin settings.")
        return
    zoom_to_code(self)

def get_expression_feature_ids(self):
    if not self.layer_id or not self.attribute:
        QMessageBox.warning(self.iface.mainWindow(), "Plugin Settings", "Layer ID and attribute must be defined in the plugin settings.")
        return
    expression = "\""+self.attribute+"\" in ("+self.ids+")";
    return expression;

def zoom_to_code(self):
    layer = QgsProject.instance().mapLayersByName(self.layer_id)[0]
    
    if not layer:
        # Show an error message if layer is not found
        QMessageBox.warning(self.iface.mainWindow(), "Layer not found", "The layer with ID {} was not found.".format(self.layer_id))
        return
    # layer = QgsProject.instance().mapLayersByName(layername)[0];
    layer.removeSelection();
    selection= layer.getFeatures(QgsFeatureRequest().setFilterExpression( get_expression_feature_ids(self) ));
    layer.selectByIds([s.id() for s in selection])
    iface.mapCanvas().zoomToSelected();
    return