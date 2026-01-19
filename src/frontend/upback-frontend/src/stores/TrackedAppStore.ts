import {defineStore} from "pinia";
import {TrackedApp} from "@/interfaces/TrackedApps";
import trackedAppsService from "@/services/TrackedAppsService";

export const useTrackedAppStore = defineStore('trackedApp', {
    state: () => ({
        trackedApp: null as TrackedApp | null
    }),
    actions: {
        setTrackedApp(trackedApp: TrackedApp) {
            this.trackedApp = trackedApp;
        },

        removeTrackedApp() {
            this.trackedApp = null;
        },

        async fetchTrackedApp(uuid: string) {
            trackedAppsService.getTrackedApp(uuid)
                .then(res => {
                    this.trackedApp = res
                })
        }
    }
})