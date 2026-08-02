def apply_theme():

    return """

<style>


/* Main Background */

.stApp{

    background:
    linear-gradient(
        135deg,
        #000000,
        #001a33
    );

    color:white;

}



/* Remove default header */

header{

    background:none !important;

}



/* Title Styling */

h1{

    color:#00aaff !important;

    font-weight:800;

}



h2,h3{

    color:#00aaff !important;

}



/* KPI Cards */


.metric-card{


    background:
    linear-gradient(
        145deg,
        #050505,
        #00264d
    );


    padding:25px;


    border-radius:18px;


    border:1px solid #007BFF;


    box-shadow:
    0 0 15px rgba(0,123,255,0.4);


    transition:0.3s;


    height:130px;


}



.metric-card:hover{


    transform:translateY(-5px);


    box-shadow:
    0 0 25px rgba(0,170,255,0.8);


}



.metric-title{


    font-size:18px;

    color:#00aaff;

}



.metric-value{


    font-size:35px;

    font-weight:bold;

    color:white;

}




/* Buttons */


.stButton>button{


    background:

    linear-gradient(
    90deg,
    #0066ff,
    #00aaff
    );


    color:white;


    border-radius:12px;


    border:none;


    height:45px;


    font-weight:bold;


}



.stButton>button:hover{


    box-shadow:
    0 0 15px #00aaff;


}




/* Dataframe */

[data-testid="stDataFrame"]{


    border-radius:15px;


}



/* Sidebar */


section[data-testid="stSidebar"]{


    background:

    linear-gradient(
    180deg,
    #000000,
    #001a33
    );


}


</style>

"""