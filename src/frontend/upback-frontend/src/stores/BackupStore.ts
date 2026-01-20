import {defineStore} from "pinia";
import {Backup} from "@/interfaces/Backups";
import BackupsService from "@/services/BackupsService";

export const useBackupStore = defineStore('backup', {
    state: () => ({
        backups: [] as Backup[]
    }),
    actions: {
        setBackups(backups: Backup[]) {
            this.backups = backups;
        },

        removeBackups() {
            this.backups = [] as Backup[];
        },

        fetchbackups(uuid: string) {
            BackupsService.getBackups(uuid)
                .then(res => {
                    this.backups = res;
                })
        }
    }
})