import m from "mithril";

const api = {
  error: "",

  get: (url) => {
    return api.request({
      method: "GET",
      url: url,
    });
  },

  request: (options) => {
    api.error = "";
    return m.request(options).catch(e => {
      console.log(e);
      if (e.code >= 400) {
        api.error = e.response.error;
        console.log(api.error);
        m.redraw();
      }

      if (e.code == 401) {
        m.route.set('/login');
        m.redraw();
      }
    });
  }
};

export default api;
