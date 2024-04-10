    var tableData = [
        ["Data 1", "Data 2"],
        ["Another Data 1", "Another Data 2"],
        ["A其他1", "A其他2"],
        ["A其他1", "A其他2"],
        ["A其他1", "A其他2"],
        ["A其他1", "A其他2"],
        ["VARCHAR", "string"]
    ];

    // 页面加载时生成初始表格
    window.onload = function() {
        generateTable();
    };

    // 根据二维数组生成表格
    function generateTable() {
        var tableBody = document.getElementById("tableBody");

        // 清空表格内容
        tableBody.innerHTML = '';

        // 遍历二维数组并生成表格行和单元格
        for (var i = 0; i < tableData.length; i++) {
            var row = document.createElement("tr");
            for (var j = 0; j < tableData[i].length; j++) {
                var cell = document.createElement("td");
                cell.textContent = tableData[i][j];
                row.appendChild(cell);
            }
            tableBody.appendChild(row);
        }
    }

//     function convertToHiveType(mysqlType) {
//     for (var i = 0; i < tableData.length; i++) {
//         if (tableData[i][0] === mysqlType) {
//             return tableData[i][1];
//         }
//     }
//     return "未找到匹配的类型"; // 如果没有找到匹配的类型映射，则返回 "UNKNOWN"，你可以根据需要修改此处的返回值
// }

    function convertFieldType(mysqlFieldType) {
    // 在静态数据中查找匹配的行
    var matchingRow = tableData.find(function(row) {
        return row[0] === mysqlFieldType;
    });

    // 如果找到匹配的行，则返回该行的第二个字段；否则返回空字符串
    var convertedType = matchingRow ? matchingRow[1] : "";

    // 返回转换后的类型
    return convertedType;
}
