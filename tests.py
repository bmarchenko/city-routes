import unittest
from routes import get_start_coordinates, parse_command, process_path

class TestRoutes(unittest.TestCase):
    """
    These are unit tests, try to test each function and keep it atomic.
    """

    def test_get_start_coordinates(self):
        """
        Test function get_start_coordinates.
        """
        self.assertEqual(get_start_coordinates("1,2"), (1,2))
        self.assertEqual(get_start_coordinates("1345,2234"), (1345,2234))
        #wrong format - not integers
        self.assertRaises(ValueError, get_start_coordinates, ",abc")
        self.assertRaises(ValueError, get_start_coordinates, "1.5,1")
        #Negative coordinates
        self.assertRaises(ValueError, get_start_coordinates, "-1,1")

    def test_parse_command(self):
        """
        Test function parse_command.
        """
        #normal GO
        self.assertEqual(parse_command(0,0, "W", "GO 5 N"), (0,5, 'N'))
        self.assertEqual(parse_command(5,5, "W", "GO 5 E"), (0,5, 'E'))

        #normal TURN
        self.assertEqual(parse_command(5,5, "W", "TURN left"), (5,5, 'N'))
        self.assertEqual(parse_command(5,5, "S", "TURN right"), (5,5, 'W'))

        #out of grid
        self.assertRaises(ValueError, parse_command, *(0,0, "W", "GO 5 E"))

        #invalid command
        self.assertRaises(ValueError, parse_command, *(0,0, "W", "GOT 5 E"))

        #not existing landmark
        self.assertRaises(ValueError, parse_command, *(0,0, "W", "GO parkour"))

    def test_process_path(self):
        """
        Test function process_path.
        """
        routes_data = {
                  "1": ["1,2", "GO 5 N", "GO 4 W", "TURN left", "GO 120"],
                  "2": ["136,20", "GO 10 S", "TURN right", "GO 100", "GO 12 W"]
                }
        self.assertEqual(process_path(routes_data, '2'), (248, 10))

        #wrong route id
        self.assertRaises(ValueError, process_path, *(routes_data, 'wrong route id'))

if __name__ == '__main__':
    unittest.main()
