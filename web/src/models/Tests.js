import m from "mithril";

import Notifications from "./Notifications.js";

const Tests = {
  list: [],

  load: (id) => {
    return m.request({
      method: "GET",
      url: "/api/ts"
    }).then(result => {
      Tests.list = result;
      Notifications.load();
    });
  },

  create: () => {
    return m.request({
      method: "POST",
      url: "/api/ts",
    }).then(() => {
      Tests.load();
    });
  },

  execute: (id) => {
    return m.request({
      method: "POST",
      url: `/api/ts/${id}/execute`,
    }).then(() => {
      Tests.load();
    });
  },

  delete: (id) => {
    return m.request({
      method: "DELETE",
      url: `/api/ts/${id}`,
    }).then(() => {
      Tests.load();
    });
  },
};

export default Tests
