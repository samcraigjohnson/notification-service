import m from "mithril";

import Notifications from "../models/Notifications.js";
import Tests from "../models/Tests.js";

class Main {
  oninit() {
    Notifications.load();
    Notifications.loadSubs();
    Tests.load();
  }

  markReadButton(notif) {
    if (!notif.read) {
      return  m(".btn.btn-blue", {
        onclick: e => {
          Notifications.markRead(notif.id);
        }
      }, "Mark read");
    }

    return ""
  }

  view(vnode) {
    return m(".my-lists", [
      m(".btn.btn-blue", {
        onclick: e => {
          Tests.create();
        },
      }, "Create Test"),
      
      m(".tests.m-5", Tests.list.map(ts => {
        return('.test', [
          m('.ts-name.text-lg', `Test scenario ${ts.id}`),

          m(".items.m-5", Object.entries(ts).map(([k, v]) => {
            return m(".item", `${k} - ${v}`);
          })),

          m(".btn.btn-blue", {
            onclick: e => {
              Tests.execute(ts.id);
            }
          }, "Execute"),

          m(".btn.btn-blue", {
            onclick: e => {
              Tests.delete(ts.id);
            }
          }, "Delete"),
        ]);
      })),

      m(".notifications.border-solid.border-4", Notifications.subs.map(sub => {
        return('.notif', [
          m(".items",  `user: ${sub.user} - event: ${sub.event.name}`),
        ]);
        
      })),

      m(".notifications.border-solid.border-4", Notifications.list.map(notif => {
        return('.notif', [
          m('.name.text-lg.mt-2', `Notif ${notif.id}`),

          m(".items",  `read: ${notif.read} - user: ${notif.user} - notification: ${notif.notification}`),

          this.markReadButton(notif),

        ]);
      })),
    ]);
  }
}

export default Main;
