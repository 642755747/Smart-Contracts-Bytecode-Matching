import os
import json
import random

now_idx = dict()

def pruning_tree(now: int, nodes_out: dict, delete_nodes: list, n_edges: list):
    global now_idx
    str_now = str(now)
    edgeslink_list = list()

    if(nodes_out.get(str_now) is not None):
        for out_node in nodes_out[str_now]:
            ret = pruning_tree(out_node, nodes_out, delete_nodes, n_edges)
            edgeslink_list = edgeslink_list + ret

    if(str_now in delete_nodes):
        return edgeslink_list
    else:
        for i in edgeslink_list:
            if([now_idx[str(now)], now_idx[str(i)]] not in n_edges):
                n_edges.append([now_idx[str(now)], now_idx[str(i)]])
        return [now]




func_path = "labeled_dataset"
func_list = os.listdir(func_path)

cnt = 0
json_num = 327871

for func in func_list:
    cnt = cnt + 1
   # print(cnt)
    pkl_path = os.path.join(func_path, func)
    pkl_list = os.listdir(pkl_path)
    divide_dataset_num = random.randint(1, 10)
    for i in pkl_list:
        data = dict()
        now_idx = dict()
        with open(os.path.join(pkl_path, i), "rb") as f:
            data = json.loads(f.readline())
            delete_nodes = f.readline().decode()
            delete_nodes_list = delete_nodes.split(" ")

        edges = data['edges']
        features = data['features']

        for num in range(0, len(features)):
            str_num = str(num)
            now_idx[str_num] = num

        for num in delete_nodes_list:
            if(num != ""):
                num = int(num)   
                for j in range(num+1, len(features)): 
                    str_j = str(j)
                    now_idx[str_j] = now_idx[str_j] - 1

        node_out = dict()
        for edge_pair in edges:
            str_edge_pair0 = str(edge_pair[0])
            str_edge_pair1 = str(edge_pair[1])
            if(node_out.get(str_edge_pair0) is None):
                node_out[str_edge_pair0] = [edge_pair[1]]
            else:
                tmp_list = node_out[str_edge_pair0]
                tmp_list.append(edge_pair[1])
                node_out[str_edge_pair0] = tmp_list

        new_edges = list()
        tmp = pruning_tree(0, node_out, delete_nodes_list, new_edges)

        # for root_out_nodes in tmp:
        #     if([now_idx["0"], now_idx[str(root_out_nodes)]] not in new_edges):
        #         print(root_out_nodes)
        #         new_edges.append([now_idx["0"], now_idx[str(root_out_nodes)]])

        new_features = dict()
        for feature in features.items():
            if(feature[0] in delete_nodes_list):
                continue
            else:
                new_features[str(now_idx[feature[0]])] = feature[1]
        new_slice = dict()
        new_slice['edges'] = new_edges
        new_slice['features'] = new_features

        # if(divide_dataset_num):
        #     vul_path = "./graph2vec/vul_dataset"
        #     dataset_func_path = os.path.join(vul_path, func)
        #     if(os.path.exists(dataset_func_path) == False):
        #         os.mkdir(dataset_func_path)
        #     with open(os.path.join(dataset_func_path, i), "w") as f:
        #         new_slice = json.dumps(new_slice)
        #         f.write(new_slice)
        #         f.close()

        if(divide_dataset_num == 1 or divide_dataset_num == 2):
            test_path = "./graph2vec/test_dataset"
            dataset_func_path = os.path.join(test_path, func)
            if(os.path.exists(dataset_func_path) == False):
                os.mkdir(dataset_func_path)
            with open(os.path.join(dataset_func_path, i), "w") as f:
                new_slice = json.dumps(new_slice)
                f.write(new_slice)
                f.close()

        if(divide_dataset_num >= 3):
            train_path = "./graph2vec/train_dataset"
            str_json = str(json_num) + ".json"
            with open(os.path.join(train_path, str_json), "w") as f:
                new_slice = json.dumps(new_slice)
                f.write(new_slice)
                f.close()
            json_num = json_num + 1
            print(json_num)
 #   break


    
    
     

