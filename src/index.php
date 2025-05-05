<?php

//load env file
# $env_file = __DIR__ . '/../.env';
// if (file_exists($env_file)) {
//     $lines = file($env_file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
//     foreach ($lines as $line) {
//         if (strpos($line, '=') !== false && strpos($line, '#') !== 0) {
//             list($key, $value) = explode('=', $line, 2);
//             putenv(trim($key)."=".trim($value));
//         }
//     }
// }
 
//database info
$servername = "sysmysql8.auburn.edu";
$username = 'jgw0052';
$password = 'Slader44!';
$dbname = "jgw0052db";

//create connection
$conn = new mysqli($servername, $username, $password, $dbname);

//check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} else {
    echo "Database connection successful!<br>";
}

//select database
$conn->select_db($dbname);

//setup output
$output = "";

//form handling
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $query = stripslashes($_POST['query']);

    //block drop queries
    if (stripos($query, 'DROP') !== false) {
        $output = "DROP statements are not allowed.";
    } else {
        if ($conn->query($query) === TRUE) {
            //check query type
            if (stripos($query, 'CREATE') === 0) {
                $output = "Table Created.";
            } elseif (stripos($query, 'UPDATE') === 0) {
                $output = "Table Updated.";
            } elseif (stripos($query, 'INSERT') === 0) {
                $output = "Row Inserted.";
            } elseif (stripos($query, 'DELETE') === 0) {
                $affected_rows = $conn->affected_rows;
                $output = "Row(s) Deleted: $affected_rows.";
            } else {
                $output = "Query executed successfully.";
            }
        } else {
            //handle select queries
            $result = $conn->query($query);
            if ($result) {
                if ($result->num_rows > 0) {
                    //build table
                    $output .= "<table border='1'><tr>";
                    //add headers
                    while ($field = $result->fetch_field()) {
                        $output .= "<th>" . htmlspecialchars($field->name) . "</th>";
                    }
                    $output .= "</tr>";

                    //add rows
                    while ($row = $result->fetch_assoc()) {
                        $output .= "<tr>";
                        foreach ($row as $value) {
                            $output .= "<td>" . htmlspecialchars($value) . "</td>";
                        }
                        $output .= "</tr>";
                    }
                    $output .= "</table>";
                    
                    //add rows retrieved message
                    $output .= "<p>Rows retrieved: " . $result->num_rows . "</p>";
                } else {
                    $output = "No results found.";
                }
            } else {
                $output = "Error: " . $conn->error;
            }
        }
    }
}

//close connection
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Joseph Williams - Final Project Demo</title>
</head>
<body>
    <h1>Final Project - Joseph Williams</h1>
    <form method="post">
        <label for="query">Query Tables</label><br>
        <textarea id="query" name="query" rows="4" cols="50"></textarea><br><br>
        <input type="submit" value="Submit">
        <input type="reset" value="Clear">
    </form>
    <br>
    <div>
        <h3>Result(s):</h3>
        <?php echo $output; ?>
    </div>
</body>
</html>