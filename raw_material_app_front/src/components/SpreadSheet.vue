<template>
  <div class="spread-sheet">
    <ul>
      <li class="btn-group">
        <i class="fa fa-trash" style="font-size:25px" @click="delRecord"></i>
        <i class="fa fa-download" style="font-size:25px" @click="generateReport"></i>
      </li>
      <li>
        <vue-excel-editor ref="grid" v-model="jsonData" @update="newRecord" @select="onSelect" filter-row>
          <vue-excel-column field="date_added" type="date" label="Дата добавления"/>
          <vue-excel-column field="name" label="Название"/>
          <vue-excel-column field="iron_amount" type="number" label="Содержание железа"/>
          <vue-excel-column field="silicon_amount" type="number" label="Содержание кремния"/>
          <vue-excel-column field="aluminum_amount" type="number" label="Содержание алюминия"/>
          <vue-excel-column field="sodium_amount" type="number" label="Содержание кальция"/>
          <vue-excel-column field="sulfur_amount" type="number" label="Содержание серы"/>
          <i class="fa fa-plus" style="font-size:15px" @click="newRow"></i>
        </vue-excel-editor>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SpreadSheet",
  data() {
    return {
      jsonData: [],
      arrayId: [],
    }
  },
  methods: {
    newRecord() {
      console.log(this.jsonData)
      fetch('http://127.0.0.1:5000/add-material', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(this.jsonData)
      }).then(response => {
        return response.json()
      }).then(data => console.log(data))
    },
    newRow() {
      this.jsonData.push({})
    },
    onSelect(selectIdArray) {
      this.arrayId = selectIdArray
    },
    delRecord() {
      this.arrayId.forEach(id => {
        let item = this.jsonData[id]
        console.log(this.arrayId)
        fetch(`http://127.0.0.1:5000/delete-material/${item['id']}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
        }).then(response => {
          this.jsonData.splice(item, 1)
          return response.json()
        }).then(data => console.log(data))
      })
    },
    generateReport() {
      let newArr = this.arrayId.map(item => this.jsonData[item].id)
      fetch('http://127.0.0.1:5000/generate-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(newArr)
      }).then(response => response).then(data => {
        window.open(data.url)
      })
    }
  },
  mounted() {
    fetch('http://127.0.0.1:5000/').then(
        response => {
          return response.json()
        }
    ).then(data => {
      data.forEach(item => this.jsonData.push(item))
    })
  }
}
</script>

<style scoped>
.spread-sheet {
  display: flex;
  justify-content: center;
}

.spread-sheet ul {
  list-style: none;
}

.btn-group {
  justify-content: space-evenly;
}
</style>