# MetaNetwork
Network ML model for MetAktiv

# Список входных данных. На вход модели подаются параметры [1-28]
# 00: 'BHP'                         -- Выгрузка VLP. (Целевой параметр)
# 01: 'GOR'                         -- Выгрузка VLP  (Входной параметр из предыдущего узла)
# 02: 'LIQ'                         -- Выгрузка VLP  (Входной параметр из предыдущего узла)
# 03: 'THP'                         -- Выгрузка VLP  (Входной параметр из предыдущего узла)
# 04: 'WCT'                         -- Выгрузка VLP  (Входной параметр из предыдущего узла)
# 05: 'angle'                       -- Угол из Deviation Survey.   (Параметр из json)
#                                      Можно определить через profileHorDistanceMSpaceHeightM в файле network.json
# 06: 'bubble_point_corr_param_1'   -- Bubble Point Parameter 1 из Correlation из PVT Input Data. Задавался 1.0
# 07: 'bubble_point_corr_param_2'   -- Bubble Point Parameter 2 из Correlation из PVT Input Data. Задавался 0.0
# 08: 'correlation'                 -- Тип корреляции VLP. Задавалс 5 (Beggs and Brill)
# 09: 'friction'                    -- Параметр корреляции для Beggs and Brill
# 10: 'gas_gravity'                 -- Gas Gravity из PVT Input Data. Задавался 0.75 (Параметр из json)
# 11: 'gravity'                     -- Параметр корреляции для Beggs and Brill
# 12: 'heat_transfer_coef'          -- Overall Heat Transfer Coefficient из Geothermal Gradient. Задавался 8
# 13: 'inner_temp'                  -- Formation Temperature из Geothermal Gradient на глубине Measured Depth. Задавался 30
# 14: 'measured_depth'              -- Measured depth из deviation survey. По сути длина трубы (Параметр из json)
#                                   -- Можно определить через profileHorDistanceMSpaceHeightM в файле network.json
# 15: 'oil_fvf_corr_param_1'        -- Oil FVF (Below Pb) Parameter 1 из Correlation из PVT Input Data. Задавался 1.0
# 16: 'oil_fvf_corr_param_2'        -- Oil FVF (Below Pb) Parameter 2 из Correlation из PVT Input Data. Задавался 0.0
# 17: 'oil_gravity'                 -- Oil Gravity из PVT Input Data. Задавался 808.47 (Параметр из json)
# 18: 'roughness'                   -- Шероховатость из Downhole Equipment. Задавался 3e-5 (Параметр из json)
# 19: 'sgor'                        -- Solution GOR из PVT Input Data. Задавался 89.27
# 20: 'sgor_corr_param_1'           -- Solution GOR Parameter 1 из Correlation из PVT Input Data. Задавался 1.0
# 21: 'sgor_corr_param_2'           -- Solution GOR Parameter 2 из Correlation из PVT Input Data. Задавался 0.0
# 22: 'surface_temp'                -- Formation Temperature из Geothermal Gradient на 0 м. Задавался 5
# 23: 'top_node_pressure'           -- Top Node Pressure из VLP. Задавлся 11.1  !!! Это же дублирование THP
# 24: 'total_gor'                   -- Total GOR из VLP. Задавался 89.27
# 25: 'tube_diametr'                -- Диаметр трубы из DownHole Equipment (Параметр из json) 
# 26: 'viscocity_corr_param_1'      -- Oil Viscocity Parameter 1 из Correlation из PVT Input Data. Задавался 1.0
# 27: 'viscocity_corr_param_2'      -- Oil Viscocity Parameter 2 из Correlation из PVT Input Data. Задавался 0.0
# 28: 'water_cut'                   -- Water Cut из VLP. Задавался 1