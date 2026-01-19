import {defineStore} from 'pinia'

export const useSSEStore = defineStore('sse', {
    state: () => ({
        syncEs: null as EventSource | null,
        nextRunEs: null as EventSource | null,
        syncProgress: {} as Record<any, any>,
        nextRun: {} as Record<any, any>
    }),

    actions: {
        startSync(url: string) {
            if (this.syncEs) return
            this.syncEs = new EventSource(url)

            this.syncEs.addEventListener("progress", (e: MessageEvent) => {
                this.syncProgress = JSON.parse(e.data)
            })
        },

        startTrackedApp(url: string) {
            if (this.nextRunEs) return
            this.nextRunEs = new EventSource(url)

            this.nextRunEs.addEventListener("next_run", (e: MessageEvent) => {
                this.nextRun = JSON.parse(e.data)
            })
        },

        stopAll() {
            this.syncEs?.close()
            this.nextRunEs?.close()
            this.syncEs = null
            this.nextRunEs = null
            this.syncProgress = {}
            this.nextRun = {}
        }
    }
})
