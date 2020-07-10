import m from "mithril";

const Notifications = {
  list: [],

  load: (id) => {
    return m.request({
      method: "GET",
      url: "/api/notifs"
    }).then(result => {
      Notifications.list = result
    });
  },

  markRead: (id) => {
    return api.request({
      method: "POST",
      url: `/api/notifs/${id}/read`
    });

    Notifications.load();
  },
};

export default Notifications
