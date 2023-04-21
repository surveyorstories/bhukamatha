"""
Model exported as python.
Name : download files
Group :
With QGIS : 32601
"""
from multiprocessing.spawn import import_main_path
from logging import _STYLES
import inspect
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProject,
                       QgsExpression,
                       QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingFeedback,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterBoolean
                       )
from qgis.utils import iface
from qgis.gui import QgsMessageBar
import processing
import os

from qgis.core import QgsMessageLog, Qgis
from qgis.processing import alg
from qgis.core import QgsVectorLayer, QgsProject, QgsVectorFileWriter, QgsField, QgsFeature, QgsGeometry, QgsFields
from PyQt5.QtCore import QVariant
from .topo_layout_box import createTopoLayers

# Get the plugin path to the current project folder
assets_folder = os.path.dirname(__file__)+"/assets/"
github_link = 'https://github.com/surveyorstories/bhukamatha/releases/download/latest_files/'


class topolayers(QgsProcessingAlgorithm):

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'images/topo.svg')))
        return icon

    def initAlgorithm(self, config=None):

        pass

    def processAlgorithm(self, parameters, context, model_feedback):

        # QgsMessageBar().pushMessage(title="Download",
        #                             text=str(parameters['update_lpm_templates_to_latest_version']), showMore="")

        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        # feedback.pushConsoleInfo('Processing completed successfully')

        feedback = QgsProcessingMultiStepFeedback(9, model_feedback)
        results = {}
        outputs = {}

        iface.mapCanvas().refresh()

# Define paths to the shapefiles
        # project = QgsProject.instance()
        # root = QgsProject.instance().layerTreeRoot()
        # path_to_folder = project.readPath("./")

        # path_to_Topology_Polygon = path_to_folder + '/TopoPolygon.gpkg'
        # path_to_Topology_Line = path_to_folder + '/TopoLine.gpkg'
        # path_to_Topology_Point = path_to_folder + '/TopoPoint.gpkg'

        # # Check if the layers exist in the project and remove them if found
        # project = QgsProject.instance()
        # layers_to_remove = project.mapLayersByName('TopoPolygon')
        # if layers_to_remove:
        #     project.removeMapLayer(layers_to_remove[0])

        # layers_to_remove = project.mapLayersByName('TopoLine')
        # if layers_to_remove:
        #     project.removeMapLayer(layers_to_remove[0])

        # layers_to_remove = project.mapLayersByName('TopoPoint')
        # if layers_to_remove:
        #     project.removeMapLayer(layers_to_remove[0])

        # # Create the layers
        # layer1 = QgsVectorLayer('polygon', 'TopoPolygon', 'memory')

        # layer2 = QgsVectorLayer('Linestring', 'TopoLine', 'memory')
        # layer3 = QgsVectorLayer('Point', 'TopoPoint', 'memory')

        # # Set the CRS of the layers to the project CRS
        # iface.mapCanvas().refresh()
        # layer1.setCrs(project.crs())
        # layer2.setCrs(project.crs())
        # layer3.setCrs(project.crs())

        # # Save the layers to the project folder
        # QgsVectorFileWriter.writeAsVectorFormat(
        #     layer1, path_to_Topology_Polygon, 'utf-8', layer1.crs(), 'gpkg')
        # QgsVectorFileWriter.writeAsVectorFormat(
        #     layer2, path_to_Topology_Line, 'utf-8', layer2.crs(), 'gpkg')
        # QgsVectorFileWriter.writeAsVectorFormat(
        #     layer3, path_to_Topology_Point, 'utf-8', layer3.crs(), 'gpkg')

        # # Add the layers to the project
        # layer1 = QgsVectorLayer(path_to_Topology_Polygon, 'TopoPolygon', 'ogr')

        # # Add the attribute field
        # layer1.startEditing()
        # layer1.addAttribute(
        #     QgsField('TopoDetail', QVariant.String, 'string', 80))
        # layer1.commitChanges()

        # project.addMapLayer(layer1, True)

        # layer2 = QgsVectorLayer(path_to_Topology_Line, 'TopoLine', 'ogr')
        # # Add the attribute field
        # iface.mapCanvas().refresh()
        # layer2.startEditing()
        # layer2.addAttribute(
        #     QgsField('TopoDetail', QVariant.String, 'string', 80))
        # layer2.commitChanges()
        # project.addMapLayer(layer2, True)

        # layer3 = QgsVectorLayer(path_to_Topology_Point, 'TopoPoint', 'ogr')
        # # Add the attribute field
        # layer3.startEditing()
        # layer3.addAttribute(
        #     QgsField('TopoDetail', QVariant.String, 'string', 80))
        # layer3.commitChanges()
        # project.addMapLayer(layer3, True)
        createTopoLayers()
        return results

    def name(self):
        return 'Create_Topo_ayers'

    def displayName(self):
        return 'Create Topo Layers'

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def createInstance(self):
        return topolayers()
