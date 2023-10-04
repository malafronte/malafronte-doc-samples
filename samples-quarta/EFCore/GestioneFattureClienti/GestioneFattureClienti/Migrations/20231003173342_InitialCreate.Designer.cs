﻿// <auto-generated />
using System;
using GestioneFattureClienti.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

#nullable disable

namespace GestioneFattureClienti.Migrations
{
    [DbContext(typeof(FattureClientiContext))]
    [Migration("20231003173342_InitialCreate")]
    partial class InitialCreate
    {
        /// <inheritdoc />
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder.HasAnnotation("ProductVersion", "7.0.11");

            modelBuilder.Entity("GestioneFattureClienti.Model.Cliente", b =>
                {
                    b.Property<int>("ClienteId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("CAP")
                        .HasColumnType("TEXT");

                    b.Property<string>("Citta")
                        .HasColumnType("TEXT");

                    b.Property<string>("Civico")
                        .HasColumnType("TEXT");

                    b.Property<string>("PartitaIVA")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("RagioneSociale")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("Via")
                        .HasColumnType("TEXT");

                    b.HasKey("ClienteId");

                    b.ToTable("Clienti");
                });

            modelBuilder.Entity("GestioneFattureClienti.Model.Fattura", b =>
                {
                    b.Property<int>("FatturaId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<int>("ClienteId")
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("Data")
                        .HasColumnType("TEXT");

                    b.Property<decimal>("Importo")
                        .HasColumnType("TEXT");

                    b.HasKey("FatturaId");

                    b.HasIndex("ClienteId");

                    b.ToTable("Fatture");
                });

            modelBuilder.Entity("GestioneFattureClienti.Model.Fattura", b =>
                {
                    b.HasOne("GestioneFattureClienti.Model.Cliente", "Cliente")
                        .WithMany("Fatture")
                        .HasForeignKey("ClienteId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Cliente");
                });

            modelBuilder.Entity("GestioneFattureClienti.Model.Cliente", b =>
                {
                    b.Navigation("Fatture");
                });
#pragma warning restore 612, 618
        }
    }
}
