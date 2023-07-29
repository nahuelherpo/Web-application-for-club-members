<script setup>
  import axios from 'axios';
  import { ref } from "vue";
  import allUrl from '../services/apiUrl'
  import { useNotification } from "@kyvg/vue3-notification";
  import { useSesionStore } from "../stores/SesionStore";

  let file = null;

  const sesion = useSesionStore();

  const months = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
  ]

  const today = new Date().toISOString().slice(0, 10);

  const payments = ref([]);

  const {notify} = useNotification();

  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

  function getPaidStateOf(paid) {
    if (paid) {
        return "PAGA";
    } else return "IMPAGA";
  }

  function getDateFormatOf(aDate) {
    let date = new Date(aDate);
    //Por alguna razon de horarios me cambia a un dia menos
    date.setDate(10);
    return date.toLocaleDateString();
  }

  function handleFileUpload() {
    file = event.target.files[0];
    console.log(file);
  }

  async function uploadReceipt(fee) {
    if (file != null) {
      try {

        const headers = {
          Authorization: `Bearer ${sesion.jwt.data}`,
          'Content-Type': 'application/json'
        };

        const file_b64 = await toBase64(file);

        const body = {
            paid_by: "Pagado por el asociado.",
            payment_date: (new Date()).toLocaleDateString('es'),
            fee_id: fee.id,
            amount_paid: fee.amount,
            image: file_b64
        };

        console.log(file)

        //Hago un post a la api con el archivo y los demas campos
        let response = await axios.post(allUrl.payments, body, { headers });
        
        if (!(response.status == 200)) {
          throw Error('Error occurs when loading data')
        }

        notify({
            title: "Pago registrado",
            type: "success"
          });
        
        load();

      } catch(e) {
        console.log("Failed to load data");
        console.log(e);
      }
    } else {
      notify({
          title: "Archivo no seleccionado",
          text: "Usted debe seleccionar un archivo para subir!",
          type: "error",
        });
    }

  }

  const load = async () => {

    try {
        
      let response = await axios({
        method: 'get',
        url: allUrl.payments,
        headers : {
          Authorization: `Bearer ${sesion.jwt.data}`
        },
        data: {
          image : "Archivo"
        }
      });

       if (!(response.status == 200)) {
        throw Error('Error occurs when loading data')
      }

      payments.value = response.data;

    } catch(e) {
        console.log("Failed to load data");
    }
  }

  load();

</script>

<template>
  <w-card class="container">
    <h3> Mis pagos al {{ today }}</h3>
    <w-divider horizontal class="mx2"></w-divider>
    <li v-for="p in payments">
      <span v-if="!p.paid">
        Cuota de {{ months[p.month - 1] }} del año {{ p.year }}, Estado {{ getPaidStateOf(p.paid) }}, VTO {{ getDateFormatOf(p.expiration_date) }}
      </span>
      <span v-else>
        Cuota de {{ months[p.month - 1] }} del año {{ p.year }}, Estado {{ getPaidStateOf(p.paid) }}
      </span>
      <div class="large-12 medium-12 small-12 cell pad2" v-if="!p.paid" >
          <w-button class="pad" @click="uploadReceipt(p)">
              Subir comprobante
          </w-button>
          <input type="file" class="pad" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </div>
    </li>
    <br/>
  </w-card>
</template>

<style scoped>
  .pad{
    margin-left: 10px;
  }
  .pad2{
    padding-top: 10px;
  }
  h3 {
    padding-top: 15px;
    padding-bottom: 15px;
    font-size: x-large;
  }
  .container{
    align-self: center;
    margin-top: 2%;
  }
</style>