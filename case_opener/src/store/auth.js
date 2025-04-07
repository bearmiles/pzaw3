// store/auth.js
const state = {
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false
  }
  
  const mutations = {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = true
    },
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    LOGOUT(state) {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
    }
  }
  
  const actions = {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/api/login/', credentials)
        commit('SET_USER', response.data.user)
        commit('SET_TOKEN', response.data.token)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async checkAuth({ commit, state }) {
      if (!state.token) return false
      
      try {
        const response = await axios.get('/api/check_auth/', {
          headers: {
            'Authorization': `Token ${state.token}`
          }
        })
        commit('SET_USER', response.data)
        return true
      } catch (error) {
        commit('LOGOUT')
        return false
      }
    },
    
    async logout({ commit }) {
      await axios.post('/api/logout/')
      commit('LOGOUT')
    }
  }