document.addEventListener('alpine:init', () => {
    Alpine.data('construction', () => {
        return {
            Delay: '',
            laborers: '',
            cash_flow: '',
            Errors: '',
            communication: '',
            Change_schedule: '',
            bid_price: '',
            scope_change: '',
            Weather_conditions: '',
            Accidents: '',

            hist: [],
            AllHist: [],
            predicted: '',
            show_prediction: '',

            tasksList: [],
            Name: '',
            Duration: '',
            AssignedTo: '',
            status: '',

            init() {

                console.log('Connected...');
                this.getHistory();
                this.showTasks();
                this.getAllHistory();
                this.showAllTasks();
            },

            getHistory() {
                axios.get('/api/historical_data/')
                    .then((response) => {
                        this.hist = response.data.historical_data;

                        console.log(response.data.historical_data[0]);
                    })
            },
            getAllHistory() {
                axios.get('/api/ALL_historical_data/')
                    .then((response) => {
                        this.AllHist = response.data.historical_data;

                        console.log(response.data.historical_data[0]);
                    })
            },

            MakePrediction() {
                axios.post('/predict', {
                    laborers: this.laborers,
                    cash_flow: this.cash_flow,
                    Errors: this.Errors,
                    communication: this.communication,
                    Change_schedule: this.Change_schedule,
                    bid_price: this.bid_price,
                    scope_change: this.scope_change,
                    Weather_conditions: this.Weather_conditions,
                    Accidents: this.Accidents
                })
                    .then((response) => {
                        // this.getHistory();
                        this.predicted = response.data.prediction;
                        this.show_prediction = 'Predicted value is: ' + response.data.prediction;
                        console.log(response.data);
                        this.SaveData()
                    })


            },
            SaveData() {
                axios.post('/upload', {
                    Delay: this.predicted,
                    laborers: this.laborers,
                    cash_flow: this.cash_flow,
                    Errors: this.Errors,
                    communication: this.communication,
                    Change_schedule: this.Change_schedule,
                    bid_price: this.bid_price,
                    scope_change: this.scope_change,
                    Weather_conditions: this.Weather_conditions,
                    Accidents: this.Accidents
                })
                    .then((response) => {
                        console.log(response.data);
                        this.getHistory();
                    })


            },

            showTasks() {
                axios.get('/api/tasks/')
                    .then((response) => {
                        this.tasksList = response.data.tasks
                        console.log(this.tasksList)
                    })
            },

            showAllTasks() {
                axios.get('/api/ALL_tasks/')
                    .then((response) => {
                        this.tasksList = response.data.tasks
                        console.log(this.tasksList)
                    })
            },

            SaveTask() {
                axios.post('/addtask', {
                    Name: this.Name,
                    Duration: this.Duration,
                    AssignedTo: this.AssignedTo,
                    status: this.status

                })
                    .then((response) => {
                        console.log(response.data);
                        this.showTasks();
                    })


            },






        }

    })
})