import pytest
import logging.config
from unittest.mock import patch, MagicMock
from settings import LOGGING_CONFIG
from app.utils.conversor import table_to_list

# Configura logging
logging.config.dictConfig(LOGGING_CONFIG)


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
    
    def hola(self):
        pass
