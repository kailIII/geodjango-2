var width = 950,
height = 650;

var projection = d3.geo.albers()
.scale(120000)
.center([22.85, 40.038]);

var path = d3.geo.path()
.projection(projection);

var svg = d3.select("body").append("svg")
.attr("width", width)
.attr("height", height);

var quantize = d3.scale.quantize()
.domain([0, 1])
.range(d3.range(9).map(function(i) { return "q" + i + "-9"; }));

var rateById = {};

d3.csv("test.csv", function(data) { data.forEach(function(d) { rateById[d.id] = +d.rate; }); });

d3.json("{{ STATIC_URL }}newnabes.json", function(error, topology) {
    var nabes = topojson.object(topology, topology.objects.temp);
                                
    svg.selectAll("path")
    .data(nabes.geometries)
    .enter().append("path")
    .attr("class", function(d) { return quantize(rateById[d.id]); })
    .attr("d", path);
        
    svg.selectAll("path")
    .data(nabes.geometries)
    .append("svg:title")
    .attr("class", function(d) { return "path " + d.id; })
    .attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
    .attr("dy", ".35em")
    .text(function(d) { return d.properties.NAME; });
    
    $("path").tipsy({gravity:'w', opacity: 0.7});
});