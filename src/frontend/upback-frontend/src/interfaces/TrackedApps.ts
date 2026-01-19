export interface TrackedApp {
    uuid: string;
    autoUpdate: boolean;
    filePath: string;
    cron: string;
}


export interface TrackedAppRequest {
    auto_update: boolean;
    file_path: string;
    cron: string;
}