# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LpmProcessingModel
                                 A QGIS plugin
 Description
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-03-12
        copyright            : (C) 2023 by SurveyoStories
        email                : surveyorstories@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


__author__ = 'SurveyoStories'
__date__ = '2023-03-12'
__copyright__ = '(C) 2023 by SurveyoStories'

# noinspection PyPep8Naming


def classFactory(iface):  # pylint: disable=invalid-name
    """Load LpmProcessingModel class from file LpmProcessingModel.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from .Bhu_Kamatha import LpmProcessingModelPlugin

    return LpmProcessingModelPlugin(iface)
