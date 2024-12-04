import pytest
import json
import logging.config
from unittest.mock import patch, MagicMock
from app.utils import setup_logging
from app.utils.conversor import table_to_list, list_to_x

# Configura logging
setup_logging()

class TestConversor:

    def test_table_to_list(self):
        
        html_input = """
                <table class="table sticky-enabled" style="margin: 0px; width: 100%;">		
				    <thead>		 		
				    	<tr style="">
                            <th>
				    		    <p class="circunscripciones"></p>
				    	    </th>
			     		    <th>
			     			    <img src="../../img/pan.png" data-toggle="tooltip" data-placement="right" title="" data-original-title="PARTIDO ACCIÓN NACIONAL">
			     		    </th>		       			 
			     		    <th>
			     			    <img src="../../img/pri.png" data-toggle="tooltip" data-placement="right" title="" data-original-title="PARTIDO REVOLUCIONARIO INSTITUCIONAL">
			     		    </th>
				        </tr>
                    </thead>
				    <tbody>
				    	<tr class="filaPartidos" style="">
				    		<td class="text-left noHover">
				    			<strong>
				    				Total de votos
				    			</strong>
				    		</td>			        
				            <td>
				            	7,651,270				            	
				            </td>				                 		        
				            <td>
				            	10,660,241				            	
				            </td>				                 
		                </tr>
				    	<tr class="filaPartidos" style="">
				    		<td class="text-left noHover">
				    			<strong>
				    				Porcentaje
				    			</strong>
				    		</td>		        
				            <td>
				            	20.89%
				            </td>				            		        
				            <td>
				            	29.10%
				            </td>				                           
		                </tr>	           
				    </tbody>
				</table>
        """

        expectedOutput = [['', '', ''], ['Total de votos', '7,651,270', '10,660,241'], ['Porcentaje', '20.89%', '29.10%']]

        output = table_to_list(html_input)

        assert output == expectedOutput
    
    def test_list_to_x_json(self):
        
        list_input = [['', '', ''], ['Total de votos', '7,651,270', '10,660,241'], ['Porcentaje', '20.89%', '29.10%']]

        expectedOutput = [
			{
				"col_1": "",
				"col_2": "",
				"col_3": ""
			},
			{
				"col_1": "Total de votos",
				"col_2": "7,651,270",
				"col_3": "10,660,241"
			},
			{
				"col_1": "Porcentaje",
				"col_2": "20.89%",
				"col_3": "29.10%"
			}
		]
     

        output = list_to_x(list_input, "JSON")
        
        expectedOutput = json.dumps(expectedOutput, sort_keys=True, indent=4)
        
        assert output == expectedOutput