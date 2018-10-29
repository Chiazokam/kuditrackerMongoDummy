
$(document).ready(function(){

	$(expense_date).focusout(function(){
		let dateInput = this.value;
		//Use moment.js to validate date input
		if (moment(dateInput, 'YYYY-MM-DD', true).format() == "Invalid date"){
			this.value = '';
			$(dateError).css('visibility', 'visible');
		}
		else {
			$(dateError).css('visibility', 'hidden');
		}
	});

	$(expense_amt).focusout(function(){
		if (this.value.indexOf(',') > -1 || this.value.indexOf('.') > -1){
			this.value = '';
			$(amountError).css('visibility', 'visible');
		}
		else if (!Number.isInteger(Number(this.value))){
			this.value = '';
			$(amountError).css('visibility', 'visible');
		}
		else {
			$(amountError).css('visibility', 'hidden');
		}
	})

	$(expense_cat).focusout(function(){
		let categoryInput = this.value; //Wasn't working without defining it seperately
		if (categoryInput == "personal" || categoryInput == "business"){
			$(categoryError).css('visibility', 'hidden');
		}
		else if ( categoryInput != "personal" || categoryInput != "business") {
			this.value = '';
			$(categoryError).css('visibility', 'visible');
		}
	});
	});

	function expenseNotification() {
				var expense_date = document.getElementById("expense_date").value;
				var expense_descr = document.getElementById("expense_descr").value;
				var expense_amt = document.getElementById("expense_amt").value;
				var expense_cat = document.getElementById("expense_cat").value;

				$.ajax({
	  				url: "http://localhost:5000/addExpense",
	  				method: "POST",
	          crossDomain : true,
	          async: false,
	  				data: {
	  					"expense_date": expense_date,
	  					"expense_amt": expense_amt,
	  					"expense_cat": expense_cat,
	  					"expense_descr": expense_descr
	  				}
	  			}).done(function (data) {
	  				if (data.expense_amt && data.expense_date && data.expense_descr && data.expense_cat) {
							swal("Good job!", `Expense of ${data.expense_amt} Added`, "success", {
	  					button: "Close",
						});
	  				}
	  				if (!data) {
	  					swal({
	  						title: "Sorry",
	  						text: 'Your Expense has NOT been saved!',
	  						type: "error"
	  					});
	  				}
	  			})
			}
