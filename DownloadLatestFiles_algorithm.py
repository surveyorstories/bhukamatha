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
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFormLayout, QLineEdit, QAction
import processing
import os
from .Add_Templates_to_Project import AddLayoutsToProject
from qgis.core import QgsMessageLog, Qgis
from qgis.processing import alg

save_action = iface.mainWindow().findChild(QAction, 'mActionSaveProject')

# Get the plugin path to the current project folder
assets_folder = os.path.dirname(__file__)+"/assets/"
github_link = 'https://github.com/surveyorstories/bhukamatha/releases/download/updated_files/'


class DownloadFiles(QgsProcessingAlgorithm):

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(
            cmd_folder, 'images/download.svg')))
        return icon

    def initAlgorithm(self, config=None):

        self.addParameter(QgsProcessingParameterBoolean(
            'update_lpm_templates_to_latest_version', 'Update LPM Templates to Latest Version', defaultValue=True))
        self.addParameter(QgsProcessingParameterBoolean(
            'update_style_files_to_latest_version', 'Update Style Files to Latest Version', defaultValue=True))

    def processAlgorithm(self, parameters, context, model_feedback):

        # save the all layers in the project
        for layer in project.mapLayers().values():
            if layer.type() == QgsMapLayerType.VectorLayer:
                layer.commitChanges()

        save_action.trigger()

        # QgsMessageBar().pushMessage(title="Download",
        #                             text=str(parameters['update_lpm_templates_to_latest_version']), showMore="")

        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        # feedback.pushConsoleInfo('Processing completed successfully')

        feedback = QgsProcessingMultiStepFeedback(9, model_feedback)
        results = {}
        outputs = {}

        # Conditional branch to Download
        if (parameters['update_lpm_templates_to_latest_version'] and parameters['update_style_files_to_latest_version']) == False:
            feedback.reportError(
                '💥 Choose any one of them to Proceed for Downloading 🤞', True)
            feedback.cancel()
        if parameters['update_lpm_templates_to_latest_version']:
            feedback.pushWarning(
                '😎 Downloading the latest LPM Templates available (Requires an active internet connection to complete the task.)')

        if parameters['update_style_files_to_latest_version']:
            feedback.pushWarning(
                '😎 Downloading the latest Style Files available (Requires an active internet connection to complete the task.)')
            styles_list = ['Polygon_Style.qml', 'Exploded_Lines_Style.qml',
<< << << < HEAD
                           'Final_Vertices_Style.qml', 'Prill_lines_Style.qml']


== == == =
                           'Final_Vertices_Style.qml', 'Prill_lines_Style.qml', 'TopoPoint_Initial_Style.qml', 'TopoPoint_Setup_Style.qml', 'TopoLine_Initial_Style.qml', 'TopoLine_Setup_Style.qml', 'TopoPolygon_Initial_Style.qml', 'TopoPolygon_Setup_Style.qml']
>> >>>> > 1abf0ae369f21beb837b5cbce2c19dbc96d1a30f

            # Downloading Style FIles
            for style in styles_list:
                alg_params= {
                    'DATA': '',
                    'METHOD': 0,  # GET
                    'OUTPUT': assets_folder + style,
                    'URL': github_link + style
                }
                outputs['Polygon_styleqml'] = processing.run(
                    'native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
                i = 0
                feedback.setCurrentStep(i+1)
                if feedback.isCanceled():
                    return {}
        # downloading templates
        if parameters['update_lpm_templates_to_latest_version']:
            templates_list = ['A3_LPM_TEMPLATE_GAUTHAMI.qpt',
                              'A4_LPM_TEMPLATE_GAUTHAMI.qpt']

            for template in templates_list:
                alg_params = {
                    'DATA': '',
                    'METHOD': 0,  # GET
                    'OUTPUT': assets_folder + template,
                    'URL': github_link + template
                }

                outputs['A4_lpm_template'] = processing.run(
                    'native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
                i = 4
                feedback.setCurrentStep(i+1)
                if feedback.isCanceled():
                    return {}

        return results

    def name(self):
        return 'download_files'

    def displayName(self):
        return 'Download Latest Files'

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return 'Optional'

    def createInstance(self):
        return DownloadFiles()
