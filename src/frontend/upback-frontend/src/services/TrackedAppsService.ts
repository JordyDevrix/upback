import axios from "axios";
import {TrackedApp, TrackedAppRequest} from "@/interfaces/TrackedApps";
import {ApiResponse} from "@/interfaces/Response";

export default {
    async getTrackedApps(): Promise<TrackedApp[]> {
        return axios.get("/api/tracked-apps")
            .then(res => {
                const trackedApps: TrackedApp[] = res.data.map((app: any) => ({
                    uuid: app.uuid,
                    autoUpdate: app.auto_update,
                    filePath: app.file_path,
                    cron: app.cron,
                }));
                return trackedApps;
            })
            .catch(err => {
                console.log(err);
                return [] as TrackedApp[];
            });
    },
    async getTrackedApp(uuid: string): Promise<TrackedApp> {
        return axios.get(`/api/tracked-apps/${uuid}`)
            .then(res => {
                console.log(res)
                const trackedApp: TrackedApp = {
                    uuid: res.data.uuid,
                    autoUpdate: res.data.auto_update,
                    filePath: res.data.file_path,
                    cron: res.data.cron,
                };

                return trackedApp;
            })
            .catch(err => {
                console.log(err);
                return {} as TrackedApp;
            });
    },
    async createBackup(uuid: string): Promise<number> {
        return axios.post(`/api/tracked-apps/sync/${uuid}`)
            .then(res => {
                return res.status;
            })
            .catch(err => {
                console.log(err);
                return err.status;
            });
    },
    async deleteTrackedApp(uuid: string): Promise<number> {
        return axios.delete(`/api/tracked-apps/${uuid}`)
            .then(res => {
                return res.status;
            })
            .catch(err => {
                console.log(err);
                return err.status;
            });
    },
    async updateTrackedApp(uuid: string, body: any): Promise<number> {
        return axios.put(`/api/tracked-apps/update/${uuid}`,
            JSON.stringify(body), {
                headers: {"Content-Type": "application/json"}
            }
        ).then(res => {
            return res.status
        }).catch(err => {
            console.log(err);
            return err.status
        })
    },
    async saveNewTrackedApp(body: TrackedAppRequest): Promise<ApiResponse> {
        return axios.post(`/api/tracked-apps`,
            JSON.stringify(body), {
                headers: {"Content-Type": "application/json"}
            }
        ).then(res => {
            const response: ApiResponse = {
                ok: true, status: res.status
            }
            return response
        }).catch(err => {
            console.log(err);
            const response: ApiResponse = {
                ok: false, status: err.status
            }
            return response
        })
    }
}

