import netCDF4 as nc
import json
import numpy as np
from pathlib import Path

def nc_to_json(nc_file_path, json_file_path):
    nc_path = Path(nc_file_path)
    
    if not nc_path.exists():
        raise FileNotFoundError(f"NC文件不存在: {nc_path}")
    
    try:
        dataset = nc.Dataset(str(nc_path), 'r')
        data_dict = {}
        
        # 获取所有变量及其值
        for var_name, variable in dataset.variables.items():
            # 处理数据
            raw_data = variable[:]
            if isinstance(raw_data, np.ndarray):
                if raw_data.dtype.kind == 'S':
                    data = [s.decode('utf-8', errors='ignore') for s in raw_data.flatten()]
                    if len(raw_data.shape) > 1:
                        data = np.array(data).reshape(raw_data.shape).tolist()
                    else:
                        data = data[0] if len(data) == 1 else data
                else:
                    data = raw_data.tolist()
            elif isinstance(raw_data, bytes):
                data = raw_data.decode('utf-8', errors='ignore')
            else:
                data = raw_data.tolist() if hasattr(raw_data, 'tolist') else raw_data
            
            # 直接存储变量值
            data_dict[var_name] = data
        
        dataset.close()
        
        # 将数据写入JSON文件
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"处理NC文件时发生错误: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        current_dir = Path(r'd:\project\self\AI\weatherBureau')
        nc_file = current_dir / 'test.nc'
        json_file = current_dir / 'output.json'
        
        nc_to_json(str(nc_file), str(json_file))
        print(f"转换成功！JSON文件已保存到: {json_file}")
    except Exception as e:
        print(f"错误: {e}")
        print("详细错误信息:")
        print(traceback.format_exc())