// add button handlers in Permutation page
// function load_permutation_button_handler(){
//     console.log($id("compute_permutation_btn"))
//     $id("compute_permutation_btn").onclick = get_perm_count;
//     $id("simulate_btn").onclick = computeOutput;
    
//     // add sort by header in output table
//     $id("output")
//         .childNodes[0]
//         .childNodes[0]
//         .childNodes[0].onclick = function(){
//             sortTable($id("output"), 0)
//         };

//     $id("output")
//         .childNodes[0]
//         .childNodes[0]
//         .childNodes[1].onclick = function(){
//             sortTable($id("output"), 1)
//         };

//     $id("output")
//         .childNodes[0]
//         .childNodes[0]
//         .childNodes[2].onclick = function(){
//             sortTable($id("output"), 2)
//         };

//     $id("output")
//         .childNodes[0]
//         .childNodes[0]
//         .childNodes[3].onclick = function(){
//             sortTable($id("output"), 3)
//         };

//     $id("output")
//         .childNodes[0]
//         .childNodes[0]
//         .childNodes[4].onclick = function(){
//             sortTable($id("output"), 4)
//         };
// }

// function get_perm_count(){
//     // run flask get number of permutations
//     output = computePermutations()["permutations"];
//     console.log(output.length);
//     $id("span_perm_count").innerHTML = output.length;
// }
