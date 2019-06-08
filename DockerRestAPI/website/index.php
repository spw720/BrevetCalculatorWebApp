<html>
    <head>
        <title>All Times and APIs</title>
    </head>

    <body>

        <form action="" method="post">
      <div>
        <button name="listAll" class="listAll">List All</button>
        <button name="listOpenOnly" class="listOpenOnly">Open Only</button>
        <button name="listCloseOnly" class="listCloseOnly">Close Only</button>
      </div>
      <div>
        <button name="listAll/csv" class="listAll/csv">List All (CSV)</button>
        <button name="listOpenOnly/csv" class="listOpenOnly/csv">Open Only (CSV)</button>
        <button name="listCloseOnly/csv" class="listCloseOnly/csv">Close Only (CSV)</button>
      </div>
      <div>
        <button name="listAll/json" class="listAll/json">List All (JSON)</button>
        <button name="listOpenOnly/json" class="listOpenOnly/json">Open Only (JSON)</button>
        <button name="listCloseOnly/json" class="listCloseOnly/json">Close Only (JSON)</button>
      </div>
        </form>
        <ul>
            <?php

            $actual_link = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
            $parameter = $_GET['quantity'];

            if (isset($_POST['listAll'])){
              $json = file_get_contents('http://laptop-service/listAll');
              $obj = json_decode($json);
	            $openTime = $obj->openTime;
	            $closeTime = $obj->closeTime;
	            echo "	Open:\n";
              foreach ($openTime as $l) {
                echo "<li>$l</li>";
              }
              echo "	Close:\n";
              foreach ($closeTime as $l) {
                echo "<li>$l</li>";
              }
            }#end of listAll

            else if (isset($_POST['listOpenOnly'])){
              $json = file_get_contents('http://laptop-service/listOpenOnly');
              $obj = json_decode($json);
  	          $openTime = $obj->openTime;
              echo "Open:\n";
              foreach ($openTime as $l) {
                  echo "<li>$l</li>";
              }
            }#end of listOpenOnly

            else if (isset($_POST['listCloseOnly'])){
              $json = file_get_contents('http://laptop-service/listCloseOnly');
              $obj = json_decode($json);
  	          $closeTime = $obj->closeTime;
  	          echo "	Close:\n";
              foreach ($closeTime as $l) {
                  echo "<li>$l</li>";
              }
            }#end of listCloseOnly

            else if (isset($_POST['listAll/json'])){
              echo file_get_contents('http://laptop-service/listAll/json');
            }#end of listAll/json

            else if (isset($_POST['listOpenOnly/json'])){
              echo file_get_contents('http://laptop-service/listOpenOnly/json');
            }#end of ListOpenOnly/json

            else if (isset($_POST['listCloseOnly/json'])){
              echo file_get_contents('http://laptop-service/listCloseOnly/json');
            }#end of listCloseOnly/json

            else if (isset($_POST['listAll/csv'])){
              echo file_get_contents('http://laptop-service/listAll/csv');
            }#end of listAll/csv

            else if (isset($_POST['listOpenOnly/csv'])){
              echo file_get_contents('http://laptop-service/listOpenOnly/csv');
            }#end of listOpenOnly/csv

            else if (isset($_POST['listCloseOnly/csv'])){
              echo file_get_contents('http://laptop-service/listCloseOnly/csv');
            }#end of listCloseOnly/csv

            ?>
        </ul>
    </body>
</html>
