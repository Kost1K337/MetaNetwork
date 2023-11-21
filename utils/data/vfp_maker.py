import win32com.client
import time
import pandas as pd
import numpy as np
from typing import List
from dataclasses import dataclass, asdict
# from vfp_table import VfpTable
from petex_request import DoSet, DoGet, DoCmd


@dataclass
class EquipmentParams():
    measured_depth: float  # длина трубы
    angle: float  # угол наклона в градусах
    roughness: float  # шероховатость трубы
    heat_transfer_coef: float  # коэффициент теплопередачи
    surface_temp: float  # температура на поверхности (depth=0)
    inner_temp: float  # температура на глубине (depth=measured_depth)


@dataclass
class PvtParams:
    sgor: float
    oil_gravity: float
    gas_gravity: float

    # Параметры корреляции
    bubble_point_corr_param_1: float
    bubble_point_corr_param_2: float
    sgor_corr_param_1: float
    sgor_corr_param_2: float
    oil_fvf_corr_param_1: float
    oil_fvf_corr_param_2: float

    viscocity_corr_param_1: float
    viscocity_corr_param_2: float


@dataclass
class VlpParams:
    top_node_pressure: float
    water_cut: float
    total_gor: float
    correlation: float


def set_bubble_point_params(param1: float, param2: float):
    DoSet("Prosper.PVT.Correl.OilBubpnt[0].F[0]", param1)
    DoSet("Prosper.PVT.Correl.OilBubpnt[0].F[1]", param2)


def set_sgor_params(param1: float, param2: float):
    DoSet("Prosper.PVT.Correl.OilSolgor[0].F[0]", param1)
    DoSet("Prosper.PVT.Correl.OilSolgor[0].F[1]", param2)


def set_oil_fvf_params(param1: float, param2: float):
    DoSet("Prosper.PVT.Correl.OilOilfvf[0].F[0]", param1)
    DoSet("Prosper.PVT.Correl.OilOilfvf[0].F[1]", param2)


def set_oil_viscocity_params(param1: float, param2: float):
    DoSet("Prosper.PVT.Correl.OilOilvis[0].F[0]", param1)
    DoSet("Prosper.PVT.Correl.OilOilvis[0].F[1]", param2)


def set_pvt_params(sgor: float, oil_gravity: float, gas_gravity: float):
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.PVT.Input.Solgor", sgor)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.PVT.Input.Api", oil_gravity)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.PVT.Input.Grvgas", gas_gravity)


def set_TCM_params(param1: float, param2: float, name):
    DoSet("PROSPER.ANL.COR.Corr[{" + str(name) + "}].A[0]", param1)
    DoSet("PROSPER.ANL.COR.Corr[{" + str(name) + "}].A[1]", param2)


def set_dev_survey_by_angle(measured_depth: float, angle: float):
    rads = np.deg2rad(angle)
    true_depth = np.cos(rads) * measured_depth
    if abs(true_depth) < 0.001:
        true_depth = 0
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Devn.Data[0].Md", 0)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Devn.Data[0].Tvd", 0)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Devn.Data[1].Md", measured_depth)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Devn.Data[1].Tvd", true_depth)


def set_downhole(depth: float, diametr: float, roughness: float):
    DoSet("PROSPER.SIN.EQP.Down.Data[1].Type", 1)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Down.Data[1].Depth", depth)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Down.Data[1].TIR", roughness)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Down.Data[1].TID", diametr)


def set_geothermal_gradient(heat_transfer_coeff: float, surf_temp: float, inner_temp: float, depth: float):
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Geo.Htc", heat_transfer_coeff)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Geo.Data[0].Md", 0)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Geo.Data[0].Tmp", surf_temp)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Geo.Data[1].Md", depth)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.SIN.EQP.Geo.Data[1].Tmp", inner_temp)


def set_rates(rates: List[float]):
    for ind, el in enumerate(rates):
        DoCmd("PROSPER.MENU.UNITS.NORSI")
        DoSet(f"PROSPER.ANL.VLP.Rates[{ind}]", el)  # rate
        #    #DoSet("PROSPER.ANL.VLP.Sens.SensDB.Sens[6].Vals["+str(i)+"]", round(np.random.uniform(1,100),3)) # wct
        #    DoSet("PROSPER.ANL.VLP.Sens.SensDB.Sens[131].Vals["+str(i)+"]", round(np.random.uniform(1,1000),3)) # gor
        #    DoSet("PROSPER.ANL.VLP.Sens.SensDB.Sens[145].Vals["+str(i)+"]", round(np.random.uniform(1,100),5)) # thp


def set_vlp_params(top_node_pressure: float, water_cut: float, total_gor: float, correlation: float):
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.ANL.VLP.Pres", top_node_pressure)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.ANL.VLP.WC", water_cut)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.ANL.VLP.GORVAL", total_gor)
    DoCmd("PROSPER.MENU.UNITS.NORSI")
    DoSet("PROSPER.ANL.VLP.TubingLabel", correlation)


def set_cases(wct: List[float], gor: List[float], thp: List[float]):
    DoSet("PROSPER.ANL.VLP.Sens.SensDB.Vars[0]", 16)  # WCT
    DoSet("PROSPER.ANL.VLP.Sens.SensDB.Vars[1]", 17)  # GOR
    DoSet("PROSPER.ANL.VLP.Sens.SensDB.Vars[2]", 27)  # THP

    for ind, val in enumerate(wct):
        DoCmd("PROSPER.MENU.UNITS.NORSI")
        DoSet(f"PROSPER.ANL.VLP.Sens.SensDB.Sens[6].Vals[{ind}]", val)

    for ind, val in enumerate(gor):
        DoCmd("PROSPER.MENU.UNITS.NORSI")
        DoSet(f"PROSPER.ANL.VLP.Sens.SensDB.Sens[131].Vals[{ind}]", val)

    for ind, val in enumerate(thp):
        DoCmd("PROSPER.MENU.UNITS.NORSI")
        DoSet(f"PROSPER.ANL.VLP.Sens.SensDB.Sens[145].Vals[{ind}]", val)


def generateVFP(
        filename,
        equipment_params: EquipmentParams,
        pvt_params: PvtParams,
        vlp_params: VlpParams,
        rates_grid: List[float],
        wct_grid: List[float],
        gor_grid: List[float],
        thp_grid: List[float],
        diameter_grid: List[float],
        friction: float,
        gravity: float,
        rates_len: int
):
    df = pd.DataFrame()
    start = time.time()


    set_downhole(
        equipment_params.measured_depth,
        0.114,
        equipment_params.roughness,
    )

    set_dev_survey_by_angle(
        equipment_params.measured_depth,
        equipment_params.angle
    )

    set_geothermal_gradient(
        equipment_params.heat_transfer_coef,
        equipment_params.surface_temp,
        equipment_params.inner_temp,
        equipment_params.measured_depth
    )


    set_pvt_params(
        pvt_params.sgor,
        pvt_params.oil_gravity,
        pvt_params.gas_gravity
    )

    set_bubble_point_params(
        pvt_params.bubble_point_corr_param_1,
        pvt_params.bubble_point_corr_param_2
    )

    set_sgor_params(
        pvt_params.sgor_corr_param_1,
        pvt_params.sgor_corr_param_2
    )

    set_oil_fvf_params(
        pvt_params.oil_fvf_corr_param_1,
        pvt_params.oil_fvf_corr_param_2
    )

    set_oil_viscocity_params(
        pvt_params.viscocity_corr_param_1,
        pvt_params.viscocity_corr_param_2
    )

    set_vlp_params(
        vlp_params.top_node_pressure,
        vlp_params.water_cut,
        vlp_params.total_gor,
        vlp_params.correlation
    )

    DoCmd("PROSPER.ANL.VLP.CALC")
    DoCmd("PROSPER.MENU.UNITS.NORSI")

    start_write_time = time.time()

    case_count = int(DoGet("PROSPER.OUT.VLP.Results.COUNT"))
    block_size = 400
    cursor_pos = 0
    bhp = np.empty(case_count * rates_len)
    while cursor_pos < case_count:
        new_cursor_pos = min(cursor_pos + block_size, case_count)
        bhp_str = DoGet(f"PROSPER.OUT.VLP.Results[{cursor_pos}:{new_cursor_pos - 1}].VLPpres[$]").split("|")[:-1]
        bhp[cursor_pos * rates_len:new_cursor_pos * rates_len] = [float(val) for val in bhp_str]
        cursor_pos = new_cursor_pos

    df = pd.DataFrame({
        'BHP': bhp,
        'THP': thp_grid,
        'WCT': wct_grid,
        'LIQ': rates_grid,
        'GOR': gor_grid,
        'tube_diameter': diameter_grid,
    })

    df = df.assign(
        **asdict(pvt_params), 
        **asdict(equipment_params), 
        **asdict(vlp_params),
        friction=friction, 
        gravity=gravity
    )

    # Save results to file
    if filename != None:
        df.to_csv('CASES_8\\' + filename + ".csv", index=False)
    print(f"Время чтения %s секунд" % (str(time.time() - start_write_time)))
    print(f"Время генерации %s секунд" % (str(time.time() - start)))
    return df


if __name__ == '__main__':
    Server = win32com.client.Dispatch("PX32.OpenServer.1")

    set_pvt_params(89.27, 808.47, 0.75)

    Pipe_length = [125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1250, 1375, 1500, 1625, 1750, 1875, 2000, 2125, 2250, 2375, 2500]

    anglee = [85, 87, 89, 90, 91, 93, 95]

    Coeffs_gravity = [0.9, 1, 1.1]

    Coeffs_friction = [0.5, 0.75, 1, 1.5, 2]

    pvt_parameters = [0.6, 2]

    pvt_parameters_2 = [-200, 200]

    Oil_density = [780, 804.44, 828.89, 853.33, 877.78, 902.22, 926.66, 951.11, 975.55, 1000]

    Gas_gravity = [0.67, 0.68, 0.70, 0.71, 0.73, 0.74, 0.76, 0.77, 0.79, 0.80]

    rates = [1, 289.64, 463.03, 553.27, 619.52, 674.11, 721.92,
             765.46, 806.21, 845.20, 883.19, 905.77, 928.35,
             966.33, 1005.32, 1046.08, 1089.61, 1137.42,
             1192.02, 1646.03]
    wct = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 98]
    gor = [20.00, 40.00, 62.92, 98.98, 155.71, 244.95, 385.33,
           606.15, 953.50, 1500.00]
    thp = [5, 6.25, 7.5, 8.75, 10, 11.25, 12.5, 13.75, 15,
           16.25, 17.5, 18.75, 20, 21.25, 22.5, 23.75, 25,
           26.25, 27.5, 28.75]
    diameter = [0.114, 0.159, 0.219, 0.273]

    wct_grid, gor_grid, thp_grid, diameter_grid, rates_grid = np.meshgrid(wct, gor, thp, diameter, rates)
    wct_grid = wct_grid.flatten()
    gor_grid = gor_grid.flatten()
    thp_grid = thp_grid.flatten()
    rates_grid = rates_grid.flatten()
    diameter_grid = diameter_grid.flatten()

    set_rates(rates)
    set_cases(wct, gor, thp)

    for i in anglee:
        for p in Pipe_length:
            equipment_params = EquipmentParams(
                measured_depth=p,
                angle=i,
                roughness=3e-5,
                heat_transfer_coef=8,
                surface_temp=5,
                inner_temp=30
            )
            for pvt in pvt_parameters:
                for pvt_2 in pvt_parameters_2:
                    pvt_params = PvtParams(
                        sgor=89.27,
                        oil_gravity=808.47,
                        gas_gravity=0.75,
                        bubble_point_corr_param_1=pvt,
                        bubble_point_corr_param_2=pvt_2,
                        sgor_corr_param_1=pvt,
                        sgor_corr_param_2=pvt_2,
                        oil_fvf_corr_param_1=pvt,
                        oil_fvf_corr_param_2=pvt_2,
                        viscocity_corr_param_1=pvt,
                        viscocity_corr_param_2=pvt_2
                    )
                    d = "BeggsandBrill"
                    vlp_params = VlpParams(
                        top_node_pressure=11.1,
                        water_cut=1,
                        total_gor=89.27,
                        correlation=5
                    )
                    for g in Coeffs_gravity:
                        for f in Coeffs_friction:
                            set_TCM_params(g, f, d)

                            default_VFP = generateVFP(
                                f'UGOL ={i}grad_Length ={p}m_{d}_Gravk ={g}_Frick={f}_PVT_Correlation_par_1 ={pvt}_PVT_Correlation_par_2 ={pvt_2}',
                                equipment_params, pvt_params, vlp_params,
                                rates_grid=rates_grid,
                                wct_grid=wct_grid,
                                gor_grid=gor_grid,
                                thp_grid=thp_grid,
                                diameter_grid=diameter_grid,
                                friction=f,
                                gravity=g,
                                rates_len=len(rates)
                            )
                            print("")

    Server = None

