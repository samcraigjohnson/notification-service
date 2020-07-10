import m from "mithril";
import api from "./api.js";

const BLANK_CARD = {
  kana: "",
  kanji: "",
  english: "",
  options: "",
  prompt: "",
  card_type: "VOCAB",
}

const Card = {
  types: {},
  list: [],
  current: Object.assign({}, BLANK_CARD),
  counts: {},

  reset: () => {
    Card.list = [];
  },

  blank: () => {
    Card.current = Object.assign({}, BLANK_CARD);
  },

  get: (id) => {
    return api.request({
      method: "GET",
      url: `/api/cards/${id}`
    }).then(result => {
      Card.current = result;
    });
  },

  getTypes: () => {
    return api.request({
      method: "GET",
      url: `/api/cards/type`
    }).then(result => {
      Card.types = result;
    });
  },

  delete: (id) => {
    return api.request({
      method: "DELETE",
      url: `/api/cards/${id}`
    });
  },

  save: () => {
    Card.update(Card.current);
  },

  loadCards: () => {
    return api.request({
      method: "GET",
      url: "/api/cards"
    }).then(result => {
      Card.list = result;
    });
  },

  loadCounts: () => {
    return api.request({
      method: "GET",
      url: "/api/cards/count"
    }).then(result => {
      Card.counts = result;
    });
  },

  update: (card) => {
    return api.request({
      method: "PUT",
      url: "/api/cards",
      body: card
    }).then(result => {
      Card.loadCards();
    });
  },
};

export default Card;
