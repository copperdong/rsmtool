import os
import numpy as np
import pandas as pd
from shutil import rmtree

from nose.tools import raises
from pandas.util.testing import assert_frame_equal

from rsmtool.container import DataContainer
from rsmtool.writer import DataWriter


class TestDataWriter:

    def test_data_container_save_files(self):

        data_sets = [{'name': 'dataset1', 'frame': pd.DataFrame(np.random.normal(size=(100, 2)),
                                                                columns=['A', 'B'])},
                     {'name': 'dataset2', 'frame': pd.DataFrame(np.random.normal(size=(120, 3)),
                                                                columns=['A', 'B', 'C'])}]

        container = DataContainer(data_sets)

        directory = 'temp_directory'
        os.makedirs(directory, exist_ok=True)

        writer = DataWriter()
        for file_type in ['json', 'csv', 'excel']:

            if file_type != 'json':

                writer.write_experiment_output(directory,
                                               container,
                                               dataframe_names=['dataset1'],
                                               file_format=file_type)
            else:
                writer.write_experiment_output(directory,
                                               container,
                                               new_names_dict={'dataset1': 'aaa'},
                                               dataframe_names=['dataset1'],
                                               file_format=file_type)

        aaa_json = pd.read_json(os.path.join(directory, 'aaa.json'))
        ds_1_csv = pd.read_csv(os.path.join(directory, 'dataset1.csv'))
        ds_1_xls = pd.read_excel(os.path.join(directory, 'dataset1.xlsx'))

        output_dir = os.listdir(directory)
        print(output_dir)
        rmtree(directory)
        assert sorted(output_dir) == sorted(['aaa.json', 'dataset1.csv', 'dataset1.xlsx'])

        assert_frame_equal(container.dataset1, aaa_json)
        assert_frame_equal(container.dataset1, ds_1_csv)
        assert_frame_equal(container.dataset1, ds_1_xls)

    @raises(KeyError)
    def test_data_container_save_wrong_format(self):

        data_sets = [{'name': 'dataset1', 'frame': pd.DataFrame(np.random.normal(size=(100, 2)),
                                                                columns=['A', 'B'])},
                     {'name': 'dataset2', 'frame': pd.DataFrame(np.random.normal(size=(120, 3)),
                                                                columns=['A', 'B', 'C'])}]

        container = DataContainer(data_sets)

        directory = 'temp_directory'

        writer = DataWriter()
        writer.write_experiment_output(directory,
                                       container,
                                       dataframe_names=['dataset1'],
                                       file_format='html')

    def test_data_container_save_files_with_id(self):

        data_sets = [{'name': 'dataset1', 'frame': pd.DataFrame(np.random.normal(size=(100, 2)),
                                                                columns=['A', 'B'])},
                     {'name': 'dataset2', 'frame': pd.DataFrame(np.random.normal(size=(120, 3)),
                                                                columns=['A', 'B', 'C'])}]

        container = DataContainer(data_sets)

        directory = 'temp_directory'
        os.makedirs(directory, exist_ok=True)

        writer = DataWriter('test')
        for file_type in ['json', 'csv', 'excel']:

            if file_type != 'json':

                writer.write_experiment_output(directory,
                                               container,
                                               dataframe_names=['dataset1'],
                                               file_format=file_type)
            else:
                writer.write_experiment_output(directory,
                                               container,
                                               new_names_dict={'dataset1': 'aaa'},
                                               dataframe_names=['dataset1'],
                                               file_format=file_type)

        aaa_json = pd.read_json(os.path.join(directory, 'test_aaa.json'))
        ds_1_csv = pd.read_csv(os.path.join(directory, 'test_dataset1.csv'))
        ds_1_xls = pd.read_excel(os.path.join(directory, 'test_dataset1.xlsx'))

        output_dir = os.listdir(directory)
        print(output_dir)
        rmtree(directory)
        assert sorted(output_dir) == sorted(['test_aaa.json',
                                             'test_dataset1.csv',
                                             'test_dataset1.xlsx'])

        assert_frame_equal(container.dataset1, aaa_json)
        assert_frame_equal(container.dataset1, ds_1_csv)
        assert_frame_equal(container.dataset1, ds_1_xls)