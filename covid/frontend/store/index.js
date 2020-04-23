import Vuex from 'vuex'
import {
  posts
} from '../api/endpoints'

import session from '../api/session';

const createStore = () => {
  return new Vuex.Store({
    state: () => ({
      results: [],
    }),
    mutations: {
      SET_VALUES ( state, data ) {
        state.results = data;
      },

    },
    actions: {
      // Get all blog posts
      async GET_VALUES({
        commit
      }) {
        const {
          data
        } = await session.get('/continent/')
        commit('SET_VALUES', data)
      },
      // Get one post
      async GET_POST({
        commit
      }) { const { data } = await session.get('/posts/')
        commit('SET_POST', data)
      },
      async GET_SAMPLE({
        commit
      }) {
        const {
          data
        } = await session.get('/sample/')
        commit('SET_SAMPLE', data)
      },
    }
  })
}

export default createStore