import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
})

export const uploadInvoice = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post('/upload', formData)
  return data
}

export const processInvoice = async (payload) => {
  const { data } = await api.post('/process', payload)
  return data
}

export const fetchHistory = async () => {
  const { data } = await api.get('/history')
  return data
}
