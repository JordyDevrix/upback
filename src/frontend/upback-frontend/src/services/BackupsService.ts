import axios from "axios";
import {Backup} from "@/interfaces/Backups";

export default {
    async getBackups(uuid: string): Promise<Backup[]> {
        return axios.get(`/api/tracked-apps/${uuid}/backups`)
            .then(res => {
                const backups: Backup[] = res.data.backups.map((backup: any) => ({
                    uuid: backup.uuid,
                    filePath: backup.file_path,
                    timestamp: backup.timestamp
                }));

                return backups;
            })
            .catch(err => {
                console.log(err);
                return [] as Backup[];
            });
    },
}