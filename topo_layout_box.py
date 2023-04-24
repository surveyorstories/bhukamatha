from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout
from qgis.PyQt.QtWidgets import QDialog,  QAction
from qgis.core import QgsVectorLayer, QgsProject, QgsVectorFileWriter, QgsField, QgsFillSymbol, QgsSingleSymbolRenderer, QgsMapLayerType
from qgis.utils import iface
from PyQt5.QtCore import QVariant
import os
import sys
import inspect
from qgis.PyQt.QtGui import QIcon

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
icon = QIcon(os.path.join(os.path.join(cmd_folder, 'images/topo.svg')))

project = QgsProject.instance()
save_action = iface.mainWindow().findChild(QAction, 'mActionSaveProject')
root = QgsProject.instance().layerTreeRoot()
assets_folder = os.path.dirname(__file__)+"/assets/"
topo_point_style_file = assets_folder + 'TopoPoint_Initial_Style.qml'
topo_line_style_file = assets_folder + 'TopoLine_Initial_Style.qml'
topo_polygon_style_file = assets_folder + 'TopoPolygon_Initial_Style.qml'
topo_polygon_setup_style_file = assets_folder + 'TopoPolygon_Setup_Style.qml'
topo_line_setup_style_file = assets_folder + 'TopoLine_Setup_Style.qml'
topo_point_setup_style_file = assets_folder + 'TopoPoint_Setup_Style.qml'
side_village_style = assets_folder + 'Side_Villages_Style.qml'


class MyForm(QDialog):
    def __init__(self, parent=None):

        super(MyForm, self).__init__(parent)
        self.setWindowTitle('Bhu Kamatha : Topo Layers')
        self.setGeometry(100, 100, 300, 200)
        # Set window icon

        self.setWindowIcon(QIcon(icon))

        layout = QVBoxLayout(self)

        button1 = QPushButton('😎 Create Topo Layers', self)
        button1.setFixedSize(200, 30)
        layout.addWidget(button1, alignment=Qt.AlignHCenter)
        button1.clicked.connect(self.create_topo_button_clicked)

        # button2 = QPushButton('Button 2', self)
        # button2.setFixedSize(200, 30)
        # layout.addWidget(button2, alignment=Qt.AlignHCenter)
        # # button2.clicked.connect(self.button_clicked)

        # button3 = QPushButton('Button 3', self)
        # button3.setFixedSize(200, 30)
        # layout.addWidget(button3, alignment=Qt.AlignHCenter)
        # button3.clicked.connect(self.setuplpms_button_clicked)
        # Add a new QHBoxLayout for the two new buttons
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        layout.addLayout(hbox)

        # Add a "Button 2" button to the new QHBoxLayout
        button4 = QPushButton('Set for LPMS', self)
        button4.setFixedSize(96, button1.height())
        button4.clicked.connect(self.setuplpms_button_clicked)
        # button4.setFixedSize(100, 30)
        hbox.addWidget(button4, alignment=Qt.AlignHCenter)
        # hbox.addWidget(button4)

        # Add a "Button 3" button to the new QHBoxLayout
        button5 = QPushButton('Revert', self)
        button5.setFixedSize(96, button1.height())
        button5.setStyleSheet("background-color: red ; color: white")
        button5.clicked.connect(self.revertlpms_button_clicked)
        # button5.setFixedSize(100, 30)
       # hbox.addWidget(button5)
        hbox.addWidget(button5, alignment=Qt.AlignHCenter)
        hbox.addStretch(1)
        layout.addLayout(hbox)
    if project.fileName():
        print('hello')

    def create_topo_button_clicked(self):
        save_action = iface.mainWindow().findChild(QAction, 'mActionSaveProject')

        # Trigger the save action
        # save_action.trigger()

        createTopoLayers()

        # QMessageBox.information(None, 'Button Clicked',
        #                         'Button 1 was clicked!')

    def setuplpms_button_clicked(self):

        setup_topo_layers()
        QMessageBox.information(None, 'Button Clicked',
                                'Button 1 was clicked!')

    def revertlpms_button_clicked(self):

        revert_topo_layers()


my_form = MyForm()


def save_project():
    QgsProject.instance().write()
   # iface.messageBar().pushMessage('Project saved')


def createTopoLayers():
    if project.fileName():

        # Trigger the save action
        save_action.trigger()
        path_to_folder = project.readPath("./")
        root = QgsProject.instance().layerTreeRoot()
        path_to_Topology_Polygon = path_to_folder + '/TopoPolygon.gpkg'
        path_to_Topology_Line = path_to_folder + '/TopoLine.gpkg'
        path_to_Topology_Point = path_to_folder + '/TopoPoint.gpkg'

        # Check if the layers exist in the project and add their names to a list
        existing_layers = []
        for layer in root.findLayers():
            if layer.name() == 'TopoPolygon':
                existing_layers.append(layer.name())
            elif layer.name() == 'TopoLine':
                existing_layers.append(layer.name())
            elif layer.name() == 'TopoPoint':
                existing_layers.append(layer.name())
        created_layers = []
        # Create the layers that don't already exist in the project
        if 'TopoPolygon' not in existing_layers:
            layer1 = QgsVectorLayer('polygon', 'TopoPolygon', 'memory')
            layer1.setCrs(project.crs())
            QgsVectorFileWriter.writeAsVectorFormat(
                layer1, path_to_Topology_Polygon, 'utf-8', layer1.crs(), 'gpkg')
            layer1 = QgsVectorLayer(
                path_to_Topology_Polygon, 'TopoPolygon', 'ogr')
            layer1.loadNamedStyle(topo_polygon_style_file)
            layer1.startEditing()
            layer1.addAttribute(
                QgsField('TopoDetail', QVariant.String, 'string', 80))
            layer1.commitChanges()
            project.addMapLayer(layer1, True)
            for createdlayer in root.findLayers():
                if createdlayer.name() == 'TopoPolygon':
                    created_layers.append(createdlayer.name())

        if 'TopoLine' not in existing_layers:
            layer2 = QgsVectorLayer('Linestring', 'TopoLine', 'memory')
            layer2.setCrs(project.crs())
            QgsVectorFileWriter.writeAsVectorFormat(
                layer2, path_to_Topology_Line, 'utf-8', layer2.crs(), 'gpkg')
            layer2 = QgsVectorLayer(path_to_Topology_Line, 'TopoLine', 'ogr')
            layer2.loadNamedStyle(topo_line_style_file)
            layer2.startEditing()
            layer2.addAttribute(
                QgsField('TopoDetail', QVariant.String, 'string', 80))
            layer2.commitChanges()
            project.addMapLayer(layer2, True)
            for createdlayer in root.findLayers():
                if createdlayer.name() == 'TopoLine':
                    created_layers.append(createdlayer.name())
        if 'TopoPoint' not in existing_layers:
            layer3 = QgsVectorLayer('Point', 'TopoPoint', 'memory')
            layer3.setCrs(project.crs())
            QgsVectorFileWriter.writeAsVectorFormat(
                layer3, path_to_Topology_Point, 'utf-8', layer3.crs(), 'gpkg')
            layer3 = QgsVectorLayer(path_to_Topology_Point, 'TopoPoint', 'ogr')
            layer3.loadNamedStyle(topo_point_style_file)
            layer3.startEditing()
            layer3.addAttribute(
                QgsField('TopoDetail', QVariant.String, 'string', 80))
            layer3.commitChanges()
            project.addMapLayer(layer3, True)
            for createdlayer in root.findLayers():
                if createdlayer.name() == 'TopoPoint':
                    created_layers.append(createdlayer.name())
            createdlayer_msgs = "The following layers are Created succesfully: \n" + \
                ",\n ".join(created_layers)
            iface.messageBar().pushMessage("Topo Layers", createdlayer_msgs, 3, 6)

        # Show a message for any existing layers

        if existing_layers:
            layer_msg = "The following layers are already exist in the project: \n" + \
                ",\n ".join(existing_layers)
            iface.messageBar().pushMessage("Existing Topo Layers", layer_msg, 3, 6)

            QMessageBox.warning(None, 'Topo Layers Already Exist',
                                layer_msg + '\n\nPlease Remove them to create the layers again')

    # save_action.trigger()
        save_project()
    else:
        # The project has not been saved, so we display an error message
        res = QMessageBox.question(None, "Save Project?", "The project has not been saved. Please save the project and try again",
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if res == QMessageBox.Yes:
            # Save the project
            save_action.trigger()
        # Execute the program
        # Add your program code here
        elif res == QMessageBox.Cancel:
            # Cancel the operation
            return


layer_names = ['TopoPolygon', 'TopoLine', 'TopoPoint']
setup_style_files = [topo_polygon_setup_style_file,
                     topo_line_setup_style_file, topo_point_setup_style_file]

side_villagelayer = "Side_Villages"


def setup_topo_layers():
    # save the all layers in the project
    for layer in project.mapLayers().values():
        if layer.type() == QgsMapLayerType.VectorLayer:
            layer.commitChanges()

    save_action.trigger()
    loaded_layer_names = []  # List to store the names of loaded layers

    for i, layer_name in enumerate(layer_names):
        layers = QgsProject.instance().mapLayersByName(layer_name)

        if layers:
            layer = layers[0]
            layer.loadNamedStyle(setup_style_files[i])
            layer.triggerRepaint()
            # Add the name of the loaded layer to the list
            loaded_layer_names.append(layer.name())

        else:
            iface.messageBar().pushMessage(f'Layer {layer_name} not found')

    # check if the side village layer exists
    if QgsProject.instance().mapLayersByName(side_villagelayer):
        # get the layer by name
        layer5 = QgsProject.instance().mapLayersByName(side_villagelayer)[0]
        layer5.loadNamedStyle(side_village_style)
        layer5.triggerRepaint()

    if loaded_layer_names:  # Check if the list of loaded layers is not empty
        iface.messageBar().pushMessage('The Following Topo Layers are set for LPM(S) Generation : ' +
                                       ', '.join(loaded_layer_names), 3, 5)
    save_project()


# revert function code is starts here:
initial_style_files = [topo_polygon_style_file,
                       topo_line_style_file, topo_point_style_file]


def revert_topo_layers():
    save_action.trigger()
    reverted_layer_names = []  # List to store the names of loaded layers
    # List to store the names of layers that could not be reverted
    not_reverted_layer_names = []
    for i, layer_name in enumerate(layer_names):
        layers = QgsProject.instance().mapLayersByName(layer_name)

        if layers:
            layer = layers[0]
            layer.loadNamedStyle(initial_style_files[i])
            layer.triggerRepaint()
            # Add the name of the loaded layer to the list
            reverted_layer_names.append(layer.name())
        else:
            not_reverted_layer_names.append(layer_name)

    # Check if the side village layer exists and revert it
    side_village_layer = QgsProject.instance().mapLayersByName(side_villagelayer)
    layer5 = None  # Define layer5 variable outside the if statement
    side_village_layer = QgsProject.instance().mapLayersByName(side_villagelayer)
    if side_village_layer:
        layer5 = side_village_layer[0]
        symbol = QgsFillSymbol.createSimple(
            {'color': '#f2a83a', 'style': 'solid', 'outline_style': 'no'})
        renderer = QgsSingleSymbolRenderer(symbol)
        layer5.setRenderer(renderer)
        # Refresh the layer to see the changes
        layer5.triggerRepaint()
        # Add the name of the side village layer to the reverted layer names
        reverted_layer_names.append(layer5.name())
    else:
        # Add layer name instead of layer5 name
        not_reverted_layer_names.append(side_villagelayer)
    # Construct a message string with the names of any layers that could not be reverted
    message = ''
    if not_reverted_layer_names:
        message = f"The following layers could not be reverted: {', '.join(not_reverted_layer_names)}. "
    if reverted_layer_names:
        message += f"The following layers were reverted: {', '.join(reverted_layer_names)}."

    # Display the message in the QGIS message bar
    if message:
        iface.messageBar().pushMessage(message)

    save_project()
