using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

namespace Velvet
{
    public static class Program
    {
        public static void Main()
        {
            Console.Write("Enter image file path: ");
            string imageFilePath = Console.ReadLine();

            MakePredictionRequest(imageFilePath).Wait();

            Console.WriteLine("\n\nHit ENTER to exit...");
            Console.ReadLine();
        }

        public static async Task MakePredictionRequest(string imageFilePath)
        {
            var client = new HttpClient();

            // Request headers
            client.DefaultRequestHeaders.Add("Prediction-Key", "7e601d52a0d14826b92d6a49a41f502d");

            // Prediction URL
            string url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/9780a20b-1b3b-46dc-960b-7c35550bcc5a/classify/iterations/velvetv2/image";

            HttpResponseMessage response;

            // Request body. 
            byte[] byteData = GetImageAsByteArray(imageFilePath);

            using (var content = new ByteArrayContent(byteData))
            {
                content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
                response = await client.PostAsync(url, content);
                var final = await response.Content.ReadAsStringAsync();

                Console.WriteLine(final);

                //Output to txt file to analyze
                StreamWriter File = new StreamWriter("C:/Users/prabh/Downloads/new/result.txt");
                File.Write(final);
                File.Close();
            }
        }

        private static byte[] GetImageAsByteArray(string imageFilePath)
        {
            FileStream fileStream = new FileStream(imageFilePath, FileMode.Open, FileAccess.Read);
            BinaryReader binaryReader = new BinaryReader(fileStream);
            return binaryReader.ReadBytes((int)fileStream.Length);
        }
    }
}