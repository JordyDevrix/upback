import axios from "axios";
import {ApiResponse} from "@/interfaces/Response";


export default {
    async getApiDetails(): Promise<ApiResponse> {
        return axios.get("/api/details")
            .then(res => {
                const response: ApiResponse = {
                    ok: true,
                    status: res.status,
                    data: res.data
                }
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

