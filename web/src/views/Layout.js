import m from "mithril";

class Layout {
  oninit() {
  }

  view(vnode) {
    return m("main.layout", [
      m("nav.menu", {
        class: "flex items-center text-sm sm:text-m my-nav"
      }, [
        m("img.logo", {
          onclick: () => {
            m.route.set("/dashboard");
          },
          class: "cursor-pointer",
          src: "/css/alpaca.png"
        }),
        m(".links", {
          class: "flex justify-end"
        }, [
            //m(m.route.Link, {class: "m-2 hover:underline text-right", href: "/cards/new"}, "New"),
            //m(m.route.Link, {class: "m-2 hover:underline", href: "/add"}, "Lookup"),
            //m(m.route.Link, {class: "m-2 hover:underline", href: "/cards"}, "Cards"),
            m(m.route.Link, {class: "m-2 hover:underline", href: "/reviews"}, `Review (${Learning.review.count})`),
            m(m.route.Link, {class: "m-2 hover:underline", href: "/lessons"}, `Learn (${Learning.lesson.count})`),
        ]),
      ]),
      m("section", vnode.children),
    ]);
  }
}

export default Layout;
