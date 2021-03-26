<template>
    <mdb-container style="padding-bottom: 20px; padding-top: 20px">  
        <!-- <nhs-header show-nav>
        </nhs-header> -->
    <nhs-table
      heading="Files Ingested Recently"
      :headers="headers"
      :data="data"
      :responsive="false">
    
    </nhs-table>
        <mdb-row style="padding-top: 20px">
            <mdb-col col=12>
                <mdb-card>
                    Placeholder
                </mdb-card>
            </mdb-col>
        </mdb-row>

    </mdb-container>
</template>

<script>

import {
    mdbRow,
    mdbCol,
    mdbContainer,
    mdbCard,
} from "mdbvue"

import { NhsTable } from 'nhsuk-frontend-vue'

export default {
    components: {
        mdbRow,
        mdbCol,
        mdbContainer,
        mdbCard,
        NhsTable
    },
    data() {
        return {
          data: [
            {
              type: 'New Files',
              number_ingested: 3
            }
          ],
          headers: [
            {
              text: 'Type',
              value: 'type'
            },
            {
              text: 'Number Ingested',
              value: 'number_ingested'
            }
          ]
        }
    }
}
</script>