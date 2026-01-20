import axios from "axios";
import {DirItem} from "@/interfaces/Files";
import {ApiResponse} from "@/interfaces/Response";


export default {
    async getDirectoryItems(path: string): Promise<DirItem[]> {
        return axios.get(`/api/file-system?path=${encodeURIComponent(path)}`)
            .then(res => {
                const items: DirItem[] = res.data.map((item: any) => ({
                    isDir: item.is_dir,
                    name: item.name,
                    path: item.path
                }));
                return items;
            })
            .catch(err => {
                console.log(err);
                return [] as DirItem[];
            });
    },
    async getAppDirectory(): Promise<ApiResponse> {
        return axios.get("/api/file-system/api-path")
            .then(res => {
                const response: ApiResponse = {
                    ok: true,
                    status: res.status,
                    data: res.data.path
                };
                return response;
            })
            .catch(err => {
                console.log(err);
                const response: ApiResponse = {
                    ok: false, status: err.status
                }
                return response
            });
    },
}

