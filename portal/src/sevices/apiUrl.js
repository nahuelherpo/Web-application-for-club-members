const baseUrl = 'http://localhost:5000/api'

const allUrl = {
  disciplines: `${baseUrl}/club/disciplines`,
  login: `${baseUrl}/auth`,
  stats: `${baseUrl}/stats`,
  statsAso: `${baseUrl}/actives`,
  statsAge: `${baseUrl}/statsage`,
  statsGender: `${baseUrl}/statsgenere`,
  allDisciplines: `${baseUrl}/allDisciplines`
}
export default allUrl
