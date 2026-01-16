import {eventBus, EVENT_KEYS} from "@/utils/eventBus";

export const requestEvents = {
    install: (router)=>{
        eventBus.on(EVENT_KEYS.REQUEST_KEY, data=>{
            console.log(data)
            if (data['type'] && data['type'] === "R_ERROR") {
               if (data['value'] && data['value']['status'] === 401) {
                  console.log('登录过期')
                  localStorage.clear();
                  router.push('/login')
               }
            }
        });
    }
};