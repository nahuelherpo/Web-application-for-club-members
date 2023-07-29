const baseUrl = 'http://localhost:5000/api'

const allUrl = {
  disciplines: `${baseUrl}/club/disciplines`,
  my_disciplines: `${baseUrl}/me/disciplines`,
  login: `${baseUrl}/auth`,
  payments: `${baseUrl}/me/payments`,
  stats: `${baseUrl}/stats`,
  statsAso: `${baseUrl}/actives`,
  statsAge: `${baseUrl}/statsage`,
  statsGender: `${baseUrl}/statsgenere`,
  allDisciplines: `${baseUrl}/allDisciplines`,
  disciplinesStats: `${baseUrl}/statsdiscipline`,
  infoContacto: `${baseUrl}/club/info`
}
export default allUrl
