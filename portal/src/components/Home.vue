<template>
  <div class="container">
    <div class="wrapper">
      <div class="text">
        <h1 class="text-h1">Bienvenido al Club de barrio de Villa Elisa</h1>
        <h3 class="text-h2">Consulta la ultima información del club</h3>
      </div>
      <img class="img" src="/img/futbol_banner.png" />
    </div>
    <div class="mt3">
      <w-flex wrap class="text-center">
        <div class="md4 pa1">
          <div class="primary--bg rounded py3">
            <w-card title="Disciplinas">
              <w-flex wrap class="text-center">
                <div class="xs4 pa1"><img src="/img/basketball.png" class="img" /></div>
                <div class="xs8 pa1"><p>Mira las disciplinas y categorias que practicamos en nuestro club.</p></div>
              </w-flex>
            </w-card>
          </div>
        </div>
        <div class="md4 pa1">
          <div class="primary--bg rounded py3">
            <w-card title="Estadisticas">
              <w-flex wrap class="text-center">
                <div class="xs4 pa1"><img src="/img/grafico-histograma.png" class="img" /></div>
                <div class="xs8 pa1">
                  <p>Mira las ultimas estadisticas sobre nuestros asociados y las disciplinas practicas en el club.</p>
                </div>
              </w-flex>
            </w-card>
          </div>
        </div>
        <div class="md4 pa1">
          <div class="primary--bg rounded py3">
            <w-card title="Mis pagos">
              <w-flex wrap class="text-center">
                <div class="xs4 pa1"><img src="/img/credit-card.png" class="img" /></div>
                <div class="xs8 pa1"><p>Revisa toda la informacion de tus pagos y tus proximos vencimientos.</p></div>
              </w-flex>
            </w-card>
          </div>
        </div>
      </w-flex>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.img {
  width: 100%;
  height: auto;
  border-radius: 10px;
}
.wrapper {
  position: relative;

  top: 10px;
  transform-origin: center;
}
.text {
  position: absolute;
  left: 30px;
  top: 80%;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.2);
}
.text-h1 {
  font-size: 1.1vw;
  color: white;
}
.text-h2 {
  font-size: 0.8vw;
  font-weight: 300;
  color: white;
}
.rounded {
  border-radius: 10px;
}
</style>
