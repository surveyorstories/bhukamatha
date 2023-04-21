from PyQt5.QtCore import QCoreApplication
from PyQt5.QtXml import QDomDocument
from qgis.core import (QgsProject, QgsLayout, QgsApplication, QgsProcessingUtils, QgsLayoutExporter, QgsProcessing, QgsProcessingParameterFile,
                       QgsReadWriteContext, QgsMapSettings, QgsProcessingAlgorithm, QgsProcessingParameterString, QgsPrintLayout,
                       QgsProcessingParameterFileDestination, QgsProcessingParameterVectorLayer,
                       QgsVectorLayer)

from qgis.gui import QgsMessageBar
from qgis.PyQt.QtGui import QIcon
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QAction
import inspect
import os
assets_folder = os.path.dirname(__file__)+"/assets/"
plugin = QgsApplication.pluginPath()
assets_folder1 = plugin + '/bhu_kamatha/assets/'

save_action = iface.mainWindow().findChild(QAction, 'mActionSaveProject')


class AddLayoutsToProject(QgsProcessingAlgorithm):
    """Creates two print layouts from two templates"""

    TEMPLATE1 = 'TEMPLATE1'
    TEMPLATE2 = 'TEMPLATE2'

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(
            cmd_folder, 'images/template.png')))
        return icon

    def initAlgorithm(self, config=None):

        # self.addParameter(
        #     QgsProcessingParameterFile(
        #         self.TEMPLATE1,
        #         self.tr('Template File 1'),
        #     )
        # )
        # self.addParameter(
        #     QgsProcessingParameterFile(
        #         self.TEMPLATE2,
        #         self.tr('Template File 2'),
        #     )
        # )

        self.addParameter(QgsProcessingParameterVectorLayer('village_final_shape_file',
                          'Village Final Shape File', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))

    def processAlgorithm(self, parameters, context, feedback):
        # save the all layers in the project
        for layer in project.mapLayers().values():
            if layer.type() == QgsMapLayerType.VectorLayer:
                layer.commitChanges()
        # save the project
        save_action.trigger()

        template1 = assets_folder + "A3_LPM_TEMPLATE_GAUTHAMI.qpt"
        template2 = assets_folder + "A4_LPM_TEMPLATE_GAUTHAMI.qpt"
        # template1 = self.parameterAsFile(parameters, 'TEMPLATE1', context)
        # template2 = self.parameterAsFile(parameters, 'TEMPLATE2', context)

        # Create the first layout from the first template
       # param_value = parameters['village_final_shape_file']
        layout_name1 = 'A3_LPM_TEMPLATE_GAUTHAMI'
        self.add_layout_from_template(
            template1,  layout_name1, parameters, context)

        # Create the second layout from the second template

        layout_name2 = 'A4_LPM_TEMPLATE_GAUTHAMI'

        self.add_layout_from_template(
            template2,  layout_name2, parameters, context)
        # QgsMessageBar().pushMessage(title="Layout",
        #                             text='Adding layouts completed', showMore="")

        return {}

    def add_layout_from_template(self, template_file, layout_name, parameters, context):
        # Remove any existing layouts with the same name
        # save_action.trigger()

        project = QgsProject.instance()

        layout_manager = project.layoutManager()
        layout = QgsPrintLayout(project)
        layouts_list = layout_manager.printLayouts()
        for l in layouts_list:
            if l.name() == layout_name:
                layout_manager.removeLayout(l)

        # Load the template from file
        with open(template_file) as f:
            template_content = f.read()
        doc = QDomDocument()
        doc.setContent(template_content)

        # Create the new layout from the template
        layout.loadFromTemplate(doc, QgsReadWriteContext())
        layout.setName(layout_name)
        layout_manager.addLayout(layout)
        param_value = parameters['village_final_shape_file']
        #cover_layer = QgsProject.instance().mapLayersByName('Calculated')[0]

        coverlayer = QgsProcessingUtils.mapLayerFromString(
            param_value, context)
        layoutmanager = QgsProject.instance().layoutManager()
        selectlayout = layoutmanager.layoutByName(layout_name)
        atlas_obj = selectlayout.atlas()
        atlas_obj.setCoverageLayer(coverlayer)
        save_action.trigger()

    def name(self):
        return 'AddLayoutsToProject'

    def displayName(self):
        return self.tr('Add LPM Templates to Project')

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return 'Optional'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return AddLayoutsToProject()
