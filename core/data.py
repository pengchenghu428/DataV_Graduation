#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> data
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/21 20:39
@Desc   ：本脚本处理和数据相关
=================================================='''
import warnings, time
warnings.filterwarnings("ignore")
import pandas as pd
from collections import defaultdict
from core.process import extend_merge_nation_year, extend_merge_nation_month
from core.process import extend_merge_type_year, extend_merge_type_month
from core.process import extend_merge_province_year
from core.process import extend_merge_company_year, extend_merge_company_month
from core.datetime import get_current_sdt
from joblib import Parallel, delayed

class DataLoader:
    def __init__(self, pdir):
        self.pdir = pdir

        self.data = defaultdict(dict)

    def read_data(self):
        # 读取 sales 数据
        sales_nation_year_df = pd.read_csv('{}/sales_nation_year.csv'.format(self.pdir))
        sales_nation_month_df = pd.read_csv('{}/sales_nation_month.csv'.format(self.pdir))
        sales_type_year_df = pd.read_csv('{}/sales_type_year.csv'.format(self.pdir))
        sales_type_month_df = pd.read_csv('{}/sales_type_month.csv'.format(self.pdir))
        sales_province_year_df = pd.read_csv('{}/sales_province_year.csv'.format(self.pdir))
        sales_company_year_df = pd.read_csv('{}/sales_company_year.csv'.format(self.pdir))
        sales_company_month_df = pd.read_csv('{}/sales_company_month.csv'.format(self.pdir))

        # 读取保有量数据
        own_nation_year_df = pd.read_csv('{}/own_nation_year.csv'.format(self.pdir))

        # 读取宏观数据
        macro_nation_year_df = pd.read_csv('{}/macro_nation_year.csv'.format(self.pdir))
        macro_province_year_df = pd.read_csv('{}/macro_province_year.csv'.format(self.pdir))

        # 读取房地产数据
        realty_nation_year_df = pd.read_csv('{}/realty_nation_year.csv'.format(self.pdir))
        realty_nation_month_df = pd.read_csv('{}/realty_nation_month.csv'.format(self.pdir))
        realty_province_year_df = pd.read_csv('{}/realty_province_year.csv'.format(self.pdir))
        realty_province_month_df = pd.read_csv('{}/realty_province_month.csv'.format(self.pdir))

        # 财政支出数据
        finance_nation_year_df = pd.read_csv('{}/finance_nation_year.csv'.format(self.pdir))
        finance_province_year_df = pd.read_csv('{}/finance_province_year.csv'.format(self.pdir))

        # 数据拼接
        print("{}: DataLoader>>数据读取开始".format(get_current_sdt()))

        def extend_merge_data(func, dfs):
            import pandas as tpd
            tpd.set_option('mode.chained_assignment', None)
            return func(dfs)

        classes = [(mode, td) for mode in ['nation', 'type', 'province', 'company'] for td in ['year', 'month']]
        _ = classes.remove(('province', 'month'))
        dfs = [[sales_nation_year_df, own_nation_year_df, macro_nation_year_df,
                realty_nation_year_df, finance_nation_year_df],
               [sales_nation_month_df, own_nation_year_df,macro_nation_year_df,
                realty_nation_year_df, realty_nation_month_df, finance_nation_year_df],
               [sales_nation_year_df, sales_type_year_df, own_nation_year_df,
                macro_nation_year_df, realty_nation_year_df, finance_nation_year_df],
               [sales_nation_year_df, sales_nation_month_df, sales_type_year_df,
                sales_type_month_df, own_nation_year_df, macro_nation_year_df,
                realty_nation_year_df, realty_nation_month_df, finance_nation_year_df],
               [sales_nation_year_df, sales_province_year_df, own_nation_year_df, macro_nation_year_df,
                macro_province_year_df, realty_nation_year_df, realty_province_year_df, finance_nation_year_df,
                finance_province_year_df],
               [sales_nation_year_df, sales_company_year_df, own_nation_year_df, macro_nation_year_df,
                realty_nation_year_df, finance_nation_year_df],
               [sales_nation_year_df, sales_nation_month_df, sales_type_year_df, sales_type_month_df,
                sales_company_year_df, sales_company_month_df, own_nation_year_df, macro_nation_year_df,
                realty_nation_year_df, realty_nation_month_df, finance_nation_year_df]]
        func = [extend_merge_nation_year, extend_merge_nation_month,
                extend_merge_type_year, extend_merge_type_month,
                extend_merge_province_year,
                extend_merge_company_year, extend_merge_company_month]

        res = Parallel(n_jobs=5)(delayed(extend_merge_data)(func[i], dfs[i]) for i in range(7))
        for i, (mode, dt) in enumerate(classes):
            self.data[mode][dt] = res[i]

        # self.data['nation']['year'] = extend_merge_nation_year(sales_nation_year_df, own_nation_year_df,
        #                                                        macro_nation_year_df, realty_nation_year_df,
        #                                                        finance_nation_year_df)
        # self.data['nation']['month'] = extend_merge_nation_month(sales_nation_month_df, own_nation_year_df,
        #                                                          macro_nation_year_df, realty_nation_year_df,
        #                                                          realty_nation_month_df, finance_nation_year_df)
        # self.data['type']['year'] = extend_merge_type_year(sales_nation_year_df, sales_type_year_df,
        #                                                    own_nation_year_df, macro_nation_year_df,
        #                                                    realty_nation_year_df, finance_nation_year_df)
        # self.data['type']['month'] = extend_merge_type_month(sales_nation_year_df, sales_nation_month_df,
        #                                                      sales_type_year_df, sales_type_month_df,
        #                                                      own_nation_year_df, macro_nation_year_df,
        #                                                      realty_nation_year_df, realty_nation_month_df,
        #                                                      finance_nation_year_df)
        # self.data['province']['year'] = extend_merge_province_year(sales_nation_year_df, sales_province_year_df,
        #                                                            own_nation_year_df, macro_nation_year_df,
        #                                                            macro_province_year_df, realty_nation_year_df,
        #                                                            realty_province_year_df, finance_nation_year_df,
        #                                                            finance_province_year_df)
        # self.data['company']['year'] = extend_merge_company_year(sales_nation_year_df, sales_company_year_df,
        #                                                          own_nation_year_df, macro_nation_year_df,
        #                                                          realty_nation_year_df, finance_nation_year_df)
        # self.data['company']['month'] = extend_merge_company_month(sales_nation_year_df, sales_nation_month_df,
        #                                                            sales_type_year_df, sales_type_month_df,
        #                                                            sales_company_year_df, sales_company_month_df,
        #                                                            own_nation_year_df, macro_nation_year_df,
        #                                                            realty_nation_year_df, realty_nation_month_df,
        #                                                            finance_nation_year_df)

        print("{}: DataLoader>>数据读取结束".format(get_current_sdt()))


    def get_data(self, mode, time_dimension, name):
        """
        获取对应数据
        :param mode: nation/type/province/company
        :param name:
        :param time_dimension: year/month
        :return:
        """
        assert mode in ['nation', 'type', 'province', 'company'], "DataLoader: 出现非法的MODE"


        tdf = self.data[mode][time_dimension]

        if mode == 'nation' or not name:
            return tdf

        tdf = tdf.loc[tdf[mode]==name].copy()
        tdf.drop(mode, axis=1, inplace=True)
        return tdf


if __name__ == "__main__":
    print("hello")
    data_loader = DataLoader('../data/raw')
    data_loader.read_data()

    print(data_loader.get_data('type', 'month', '大').head(20))