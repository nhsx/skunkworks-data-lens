export function isEmpty(value) {
    return value === undefined || value === null || value === "";
}

export function prettifyDate(date){
    if(!date){
      return "No date found"
    }
    if (new Date(date).toLocaleString()!== "Invalid Date"){
      return new Date(date).toLocaleString();
    }
    else {
      return date;
    }
}