async function loadHealth(){

    try{

        const response=await fetch("/health");

        const data=await response.json();

        document.getElementById("api-status").innerHTML=
            "🟢 "+data.api;

        document.getElementById("db-status").innerHTML=
            "🟢 "+data.database;

        document.getElementById("persons-count").innerHTML=
            data.persons;

        document.getElementById("aliases-count").innerHTML=
            data.aliases;

        document.getElementById("passports-count").innerHTML=
            data.passports;

        document.getElementById("addresses-count").innerHTML=
            data.addresses;

        document.getElementById("amendments-count").innerHTML=
            data.amendments;

        document.getElementById("last-update").innerHTML=
            new Date().toLocaleTimeString();

    }

    catch(error){

        document.getElementById("api-status").innerHTML=
            "🔴 Offline";

        document.getElementById("db-status").innerHTML=
            "🔴 Offline";

    }

}

loadHealth();

setInterval(loadHealth,10000);