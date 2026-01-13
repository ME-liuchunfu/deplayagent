import router from "@/router/index";

export const commonRouter = {
    goto(path){
        if (path) {
            router.push(path)
        }
    }
}